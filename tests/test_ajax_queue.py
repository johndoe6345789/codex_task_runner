"""Tests for AJAX Queue in PyQt6."""
import pytest
import time


@pytest.fixture
def qt_app():
    """Create QApplication for tests."""
    from PyQt6.QtWidgets import QApplication
    import sys
    existing = QApplication.instance()
    if existing:
        yield existing
    else:
        app = QApplication(sys.argv)
        yield app


def test_ajax_queue_add_request(qt_app):
    """Test adding requests to the queue."""
    from codex_task_runner.ui.services.ajax_queue import AjaxQueue
    
    queue = AjaxQueue()
    
    # Add a request
    request_id = queue.addRequest("Test request")
    
    assert request_id is not None
    assert len(request_id) == 8
    assert queue.pending == 1
    assert queue.completed == 0
    assert queue.failed == 0
    assert queue.visible is True


def test_ajax_queue_mark_success(qt_app):
    """Test marking a request as successful."""
    from codex_task_runner.ui.services.ajax_queue import AjaxQueue
    
    queue = AjaxQueue()
    request_id = queue.addRequest("Test request")
    
    queue.markSuccess(request_id)
    
    assert queue.pending == 0
    assert queue.completed == 1
    assert queue.failed == 0


def test_ajax_queue_mark_error(qt_app):
    """Test marking a request as failed."""
    from codex_task_runner.ui.services.ajax_queue import AjaxQueue
    
    queue = AjaxQueue()
    request_id = queue.addRequest("Test request")
    
    queue.markError(request_id, "Test error message")
    
    assert queue.pending == 0
    assert queue.completed == 0
    assert queue.failed == 1


def test_ajax_queue_multiple_requests(qt_app):
    """Test handling multiple requests."""
    from codex_task_runner.ui.services.ajax_queue import AjaxQueue
    
    queue = AjaxQueue()
    
    id1 = queue.addRequest("Request 1")
    id2 = queue.addRequest("Request 2")
    id3 = queue.addRequest("Request 3")
    
    assert queue.pending == 3
    assert queue.total == 3
    
    queue.markSuccess(id1)
    assert queue.pending == 2
    assert queue.completed == 1
    
    queue.markError(id2, "Error")
    assert queue.pending == 1
    assert queue.completed == 1
    assert queue.failed == 1


def test_ajax_queue_clear_completed(qt_app):
    """Test clearing completed requests."""
    from codex_task_runner.ui.services.ajax_queue import AjaxQueue
    
    queue = AjaxQueue()
    
    id1 = queue.addRequest("Request 1")
    id2 = queue.addRequest("Request 2")
    
    queue.markSuccess(id1)
    queue.markError(id2, "Error")
    
    assert queue.total == 2
    
    queue.clearCompleted()
    
    assert queue.total == 0


def test_ajax_queue_progress(qt_app):
    """Test updating request progress."""
    from codex_task_runner.ui.services.ajax_queue import AjaxQueue
    
    queue = AjaxQueue()
    request_id = queue.addRequest("Download", progress_current=0, progress_total=100)
    
    queue.updateProgress(request_id, 50, 100)
    
    # The progress should be updated in the model
    stats = queue._model.get_stats()
    assert stats["pending"] == 1


def test_tracked_request_context_manager(qt_app):
    """Test the tracked_request context manager."""
    from codex_task_runner.ui.services.ajax_queue import AjaxQueue, tracked_request
    
    queue = AjaxQueue()
    
    # Test successful request
    with tracked_request(queue, "Test operation") as req:
        assert queue.pending == 1
        assert req.request_id is not None
    
    assert queue.pending == 0
    assert queue.completed == 1


def test_tracked_request_with_exception(qt_app):
    """Test the tracked_request context manager with an exception."""
    from codex_task_runner.ui.services.ajax_queue import AjaxQueue, tracked_request
    
    queue = AjaxQueue()
    
    try:
        with tracked_request(queue, "Failing operation"):
            raise ValueError("Test error")
    except ValueError:
        pass
    
    assert queue.pending == 0
    assert queue.completed == 0
    assert queue.failed == 1


def test_ajax_request_elapsed_time(qt_app):
    """Test elapsed time calculation."""
    from codex_task_runner.ui.services.ajax_queue import AjaxRequest, RequestStatus
    
    req = AjaxRequest(id="test", label="Test")
    time.sleep(0.1)  # 100ms
    
    elapsed = req.elapsed_ms
    assert elapsed >= 100
    assert elapsed < 200  # Should be around 100ms


def test_ajax_queue_model_roles(qt_app):
    """Test that the model exposes correct roles."""
    from codex_task_runner.ui.services.ajax_queue import AjaxQueueModel
    
    model = AjaxQueueModel()
    roles = model.roleNames()
    
    assert b"requestId" in roles.values()
    assert b"label" in roles.values()
    assert b"status" in roles.values()
    assert b"elapsed" in roles.values()
    assert b"error" in roles.values()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
