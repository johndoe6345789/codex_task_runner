"""AJAX Queue for PyQt6 - tracks and manages network requests."""
from PyQt6.QtCore import (
    QObject, pyqtSignal, pyqtSlot, pyqtProperty,
    QAbstractListModel, QModelIndex, Qt, QTimer
)
from dataclasses import dataclass, field
from typing import Optional, Callable, Any
from enum import Enum
import time
import uuid
from threading import Lock


class RequestStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class AjaxRequest:
    """Represents a tracked AJAX request."""
    id: str
    label: str
    status: RequestStatus = RequestStatus.PENDING
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    error: Optional[str] = None
    progress_current: int = 0
    progress_total: int = 0
    group: Optional[str] = None
    
    @property
    def elapsed_ms(self) -> int:
        end = self.end_time or time.time()
        return int((end - self.start_time) * 1000)
    
    @property
    def elapsed_str(self) -> str:
        elapsed = self.elapsed_ms
        if elapsed < 1000:
            return f"{elapsed}ms"
        return f"{elapsed / 1000:.1f}s"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "label": self.label,
            "status": self.status.value,
            "elapsed": self.elapsed_str,
            "error": self.error or "",
            "progress_current": self.progress_current,
            "progress_total": self.progress_total,
            "has_progress": self.progress_total > 0,
            "group": self.group or "",
        }


class AjaxQueueModel(QAbstractListModel):
    """Qt Model for the AJAX queue, exposes requests to QML."""
    
    # Roles for QML access
    IdRole = Qt.ItemDataRole.UserRole + 1
    LabelRole = Qt.ItemDataRole.UserRole + 2
    StatusRole = Qt.ItemDataRole.UserRole + 3
    ElapsedRole = Qt.ItemDataRole.UserRole + 4
    ErrorRole = Qt.ItemDataRole.UserRole + 5
    ProgressCurrentRole = Qt.ItemDataRole.UserRole + 6
    ProgressTotalRole = Qt.ItemDataRole.UserRole + 7
    HasProgressRole = Qt.ItemDataRole.UserRole + 8
    GroupRole = Qt.ItemDataRole.UserRole + 9
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._requests: list[AjaxRequest] = []
        self._lock = Lock()
    
    def roleNames(self):
        return {
            self.IdRole: b"requestId",
            self.LabelRole: b"label",
            self.StatusRole: b"status",
            self.ElapsedRole: b"elapsed",
            self.ErrorRole: b"error",
            self.ProgressCurrentRole: b"progressCurrent",
            self.ProgressTotalRole: b"progressTotal",
            self.HasProgressRole: b"hasProgress",
            self.GroupRole: b"group",
        }
    
    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._requests)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._requests):
            return None
        
        # Return in reverse order (newest first)
        req = self._requests[-(index.row() + 1)]
        
        if role == self.IdRole:
            return req.id
        elif role == self.LabelRole:
            return req.label
        elif role == self.StatusRole:
            return req.status.value
        elif role == self.ElapsedRole:
            return req.elapsed_str
        elif role == self.ErrorRole:
            return req.error or ""
        elif role == self.ProgressCurrentRole:
            return req.progress_current
        elif role == self.ProgressTotalRole:
            return req.progress_total
        elif role == self.HasProgressRole:
            return req.progress_total > 0
        elif role == self.GroupRole:
            return req.group or ""
        return None
    
    def add_request(self, request: AjaxRequest):
        """Add a new request to the queue."""
        with self._lock:
            self.beginInsertRows(QModelIndex(), 0, 0)
            self._requests.append(request)
            self.endInsertRows()
    
    def update_request(self, request_id: str, **updates):
        """Update a request's properties."""
        with self._lock:
            for i, req in enumerate(self._requests):
                if req.id == request_id:
                    for key, value in updates.items():
                        if hasattr(req, key):
                            setattr(req, key, value)
                    # Notify QML of change (reversed index)
                    qml_index = len(self._requests) - 1 - i
                    model_index = self.createIndex(qml_index, 0)
                    self.dataChanged.emit(model_index, model_index)
                    return True
        return False
    
    def remove_completed(self, older_than_ms: int = 2000):
        """Remove completed requests older than specified time."""
        cutoff = time.time() - (older_than_ms / 1000)
        with self._lock:
            to_remove = []
            for i, req in enumerate(self._requests):
                if req.status != RequestStatus.PENDING and req.end_time and req.end_time < cutoff:
                    to_remove.append(i)
            
            if to_remove:
                self.beginResetModel()
                self._requests = [r for i, r in enumerate(self._requests) if i not in to_remove]
                self.endResetModel()
    
    def clear_all(self):
        """Clear all non-pending requests."""
        with self._lock:
            self.beginResetModel()
            self._requests = [r for r in self._requests if r.status == RequestStatus.PENDING]
            self.endResetModel()
    
    def get_stats(self) -> dict:
        """Get queue statistics."""
        pending = sum(1 for r in self._requests if r.status == RequestStatus.PENDING)
        success = sum(1 for r in self._requests if r.status == RequestStatus.SUCCESS)
        error = sum(1 for r in self._requests if r.status == RequestStatus.ERROR)
        return {
            "pending": pending,
            "completed": success,
            "failed": error,
            "total": len(self._requests),
        }


class AjaxQueue(QObject):
    """Main AJAX Queue controller for PyQt6."""
    
    # Signals
    requestAdded = pyqtSignal(str)  # request_id
    requestUpdated = pyqtSignal(str)  # request_id
    requestCompleted = pyqtSignal(str, bool)  # request_id, success
    queueChanged = pyqtSignal()
    visibilityChanged = pyqtSignal(bool)
    statsChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = AjaxQueueModel(self)
        self._visible = False
        self._auto_hide_timer = QTimer(self)
        self._auto_hide_timer.setSingleShot(True)
        self._auto_hide_timer.timeout.connect(self._on_auto_hide)
        self._cleanup_timer = QTimer(self)
        self._cleanup_timer.timeout.connect(self._cleanup)
        self._cleanup_timer.start(1000)  # Check every second
    
    @pyqtProperty(QObject, constant=True)
    def model(self) -> AjaxQueueModel:
        return self._model
    
    @pyqtProperty(bool, notify=visibilityChanged)
    def visible(self) -> bool:
        return self._visible
    
    @pyqtSlot(bool)
    def setVisible(self, visible: bool):
        if self._visible != visible:
            self._visible = visible
            self.visibilityChanged.emit(visible)
    
    @pyqtProperty(int, notify=statsChanged)
    def pending(self) -> int:
        return self._model.get_stats()["pending"]
    
    @pyqtProperty(int, notify=statsChanged)
    def completed(self) -> int:
        return self._model.get_stats()["completed"]
    
    @pyqtProperty(int, notify=statsChanged)
    def failed(self) -> int:
        return self._model.get_stats()["failed"]
    
    @pyqtProperty(int, notify=statsChanged)
    def total(self) -> int:
        return self._model.get_stats()["total"]
    
    @pyqtSlot(str, result=str)
    @pyqtSlot(str, str, result=str)
    @pyqtSlot(str, str, int, int, result=str)
    def addRequest(self, label: str, group: str = "", 
                   progress_current: int = 0, progress_total: int = 0) -> str:
        """Add a new request to track. Returns the request ID."""
        request = AjaxRequest(
            id=str(uuid.uuid4())[:8],
            label=label,
            group=group or None,
            progress_current=progress_current,
            progress_total=progress_total,
        )
        self._model.add_request(request)
        self.setVisible(True)
        self._cancel_auto_hide()
        self.requestAdded.emit(request.id)
        self.queueChanged.emit()
        self.statsChanged.emit()
        return request.id
    
    @pyqtSlot(str, str)
    def updateLabel(self, request_id: str, label: str):
        """Update request label."""
        self._model.update_request(request_id, label=label)
        self.requestUpdated.emit(request_id)
    
    @pyqtSlot(str, int, int)
    def updateProgress(self, request_id: str, current: int, total: int):
        """Update request progress."""
        self._model.update_request(
            request_id,
            progress_current=current,
            progress_total=total
        )
        self.requestUpdated.emit(request_id)
    
    @pyqtSlot(str)
    def markSuccess(self, request_id: str):
        """Mark a request as successful."""
        self._model.update_request(
            request_id,
            status=RequestStatus.SUCCESS,
            end_time=time.time()
        )
        self.requestCompleted.emit(request_id, True)
        self.queueChanged.emit()
        self.statsChanged.emit()
        self._schedule_auto_hide()
    
    @pyqtSlot(str)
    @pyqtSlot(str, str)
    def markError(self, request_id: str, error: str = ""):
        """Mark a request as failed."""
        self._model.update_request(
            request_id,
            status=RequestStatus.ERROR,
            error=error,
            end_time=time.time()
        )
        self.requestCompleted.emit(request_id, False)
        self.queueChanged.emit()
        self.statsChanged.emit()
        self._schedule_auto_hide()
    
    @pyqtSlot()
    def clearCompleted(self):
        """Clear all completed/failed requests."""
        self._model.clear_all()
        self.queueChanged.emit()
        self.statsChanged.emit()
        if self.pending == 0:
            self.setVisible(False)
    
    @pyqtSlot()
    def hide(self):
        """Hide the queue widget (only if no pending requests)."""
        if self.pending == 0:
            self.setVisible(False)
    
    def _schedule_auto_hide(self):
        """Schedule auto-hide after requests complete."""
        if self.pending == 0:
            self._auto_hide_timer.start(3000)  # 3 seconds
    
    def _cancel_auto_hide(self):
        """Cancel pending auto-hide."""
        self._auto_hide_timer.stop()
    
    def _on_auto_hide(self):
        """Auto-hide callback."""
        if self.pending == 0:
            # Remove old completed requests
            self._model.remove_completed(2000)
            self.statsChanged.emit()
            if self._model.rowCount() == 0:
                self.setVisible(False)
    
    def _cleanup(self):
        """Periodic cleanup of old requests."""
        old_count = self._model.rowCount()
        self._model.remove_completed(5000)  # Remove after 5 seconds
        if self._model.rowCount() != old_count:
            self.statsChanged.emit()
            if self._model.rowCount() == 0 and self.pending == 0:
                self.setVisible(False)


class TrackedRequest:
    """Context manager for tracking a request."""
    
    def __init__(self, queue: AjaxQueue, label: str, group: str = ""):
        self.queue = queue
        self.label = label
        self.group = group
        self.request_id: Optional[str] = None
    
    def __enter__(self) -> "TrackedRequest":
        self.request_id = self.queue.addRequest(self.label, self.group)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.queue.markError(self.request_id, str(exc_val))
        else:
            self.queue.markSuccess(self.request_id)
        return False
    
    def update_progress(self, current: int, total: int):
        """Update progress during the request."""
        if self.request_id:
            self.queue.updateProgress(self.request_id, current, total)
    
    def update_label(self, label: str):
        """Update the label during the request."""
        if self.request_id:
            self.queue.updateLabel(self.request_id, label)


def tracked_request(queue: AjaxQueue, label: str, group: str = "") -> TrackedRequest:
    """Create a tracked request context manager."""
    return TrackedRequest(queue, label, group)
