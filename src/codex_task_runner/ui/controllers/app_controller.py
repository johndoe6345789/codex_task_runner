"""Main application controller exposed to QML."""
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QTimer, QVariant
from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
import json


class EnvironmentModel(QAbstractListModel):
    """Model for environment list."""
    
    IdRole = Qt.ItemDataRole.UserRole + 1
    NameRole = Qt.ItemDataRole.UserRole + 2
    FullNameRole = Qt.ItemDataRole.UserRole + 3
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._environments = []
    
    def roleNames(self):
        return {
            self.IdRole: b"envId",
            self.NameRole: b"name",
            self.FullNameRole: b"fullName",
        }
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._environments)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._environments):
            return None
        
        env = self._environments[index.row()]
        if role == self.IdRole:
            return env.get("id") or env.get("environment_id", "")
        elif role == self.NameRole:
            return env.get("name") or env.get("full_name", "")
        elif role == self.FullNameRole:
            return env.get("full_name") or env.get("name", "")
        return None
    
    def set_environments(self, envs):
        self.beginResetModel()
        self._environments = envs
        self.endResetModel()
    
    def get_environment(self, index):
        if 0 <= index < len(self._environments):
            return self._environments[index]
        return None
    
    def get_all(self):
        return self._environments


class TaskModel(QAbstractListModel):
    """Model for task list."""
    
    IdRole = Qt.ItemDataRole.UserRole + 1
    TitleRole = Qt.ItemDataRole.UserRole + 2
    StatusRole = Qt.ItemDataRole.UserRole + 3
    RepoRole = Qt.ItemDataRole.UserRole + 4
    BranchRole = Qt.ItemDataRole.UserRole + 5
    CreatedRole = Qt.ItemDataRole.UserRole + 6
    AliasRole = Qt.ItemDataRole.UserRole + 7
    PrUrlRole = Qt.ItemDataRole.UserRole + 8
    HasPrRole = Qt.ItemDataRole.UserRole + 9
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tasks = []
    
    def roleNames(self):
        return {
            self.IdRole: b"taskId",
            self.TitleRole: b"title",
            self.StatusRole: b"status",
            self.RepoRole: b"repo",
            self.BranchRole: b"branch",
            self.CreatedRole: b"created",
            self.AliasRole: b"alias",
            self.PrUrlRole: b"prUrl",
            self.HasPrRole: b"hasPr",
        }
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._tasks)
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._tasks):
            return None
        
        task = self._tasks[index.row()]
        if role == self.IdRole:
            return task.get("id", "")
        elif role == self.TitleRole:
            return task.get("title", "Untitled")
        elif role == self.StatusRole:
            return task.get("status", "unknown")
        elif role == self.RepoRole:
            return task.get("repository", {}).get("full_name", "")
        elif role == self.BranchRole:
            return task.get("head_branch", "")
        elif role == self.CreatedRole:
            return task.get("created_at", "")[:10] if task.get("created_at") else ""
        elif role == self.AliasRole:
            return str(index.row() + 1)
        elif role == self.PrUrlRole:
            pr = task.get("pull_request") or {}
            return pr.get("html_url") or pr.get("url", "")
        elif role == self.HasPrRole:
            return bool(task.get("pull_request"))
        return None
    
    def set_tasks(self, tasks):
        self.beginResetModel()
        self._tasks = tasks
        self.endResetModel()
    
    def get_task(self, index):
        if 0 <= index < len(self._tasks):
            return self._tasks[index]
        return None


class AppController(QObject):
    """Main controller for the application."""
    
    tasksLoaded = pyqtSignal()
    taskDetailLoaded = pyqtSignal(str)  # JSON string
    errorOccurred = pyqtSignal(str)
    statusMessage = pyqtSignal(str)
    patchReady = pyqtSignal(str)
    environmentsLoaded = pyqtSignal('QVariantList')
    promptSuccess = pyqtSignal(str)  # task_id
    promptError = pyqtSignal(str)  # error message
    nerdModeChanged = pyqtSignal(bool)
    debugLog = pyqtSignal(str)  # debug messages for nerd mode
    sessionInfoChanged = pyqtSignal(str)  # session info JSON
    themeChanged = pyqtSignal(str)  # theme ID
    languageChanged = pyqtSignal(str)  # language ID
    
    def __init__(self, session=None, parent=None):
        super().__init__(parent)
        self._session = session
        self._task_model = TaskModel(self)
        self._env_model = EnvironmentModel(self)
        self._current_task = None
        self._poll_timer = QTimer(self)
        self._poll_timer.timeout.connect(self._poll_tasks)
        self._environments = []
        self._nerd_mode = False
        self._debug_logs = []
        self._start_time = None
        self._theme = "system"
        self._language = "en"
        self._settings_file = self._get_settings_path()
    
    @pyqtProperty(QObject, constant=True)
    def taskModel(self):
        return self._task_model
    
    @pyqtProperty(QObject, constant=True)
    def envModel(self):
        return self._env_model
    
    @pyqtProperty(bool, notify=nerdModeChanged)
    def nerdMode(self):
        return self._nerd_mode
    
    @pyqtSlot(bool)
    def setNerdMode(self, enabled):
        """Toggle nerd mode."""
        self._nerd_mode = enabled
        self.nerdModeChanged.emit(enabled)
        if enabled:
            self._log("🤓 Nerd mode activated")
            self._emit_session_info()
        else:
            self._log("Nerd mode deactivated")
    
    def _get_settings_path(self):
        """Get path to settings file."""
        from pathlib import Path
        config_dir = Path.home() / ".config" / "codex-task-runner"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "settings.json"
    
    def _load_settings(self):
        """Load settings from file."""
        try:
            if self._settings_file.exists():
                return json.loads(self._settings_file.read_text())
        except Exception:
            pass
        return {}
    
    def _save_settings(self, settings):
        """Save settings to file."""
        try:
            self._settings_file.write_text(json.dumps(settings, indent=2))
        except Exception as e:
            self._log(f"Failed to save settings: {e}")
    
    @pyqtSlot(str)
    def setTheme(self, themeId):
        """Set and persist the theme."""
        self._theme = themeId
        settings = self._load_settings()
        settings["theme"] = themeId
        self._save_settings(settings)
        self.themeChanged.emit(themeId)
        self._log(f"🎨 Theme changed to: {themeId}")
        self.statusMessage.emit(f"Theme: {themeId}")
    
    @pyqtSlot(result=str)
    def getSavedTheme(self):
        """Get the saved theme from settings."""
        settings = self._load_settings()
        return settings.get("theme", "system")
    
    @pyqtSlot(str)
    def setLanguage(self, langId):
        """Set and persist the language."""
        self._language = langId
        settings = self._load_settings()
        settings["language"] = langId
        self._save_settings(settings)
        self.languageChanged.emit(langId)
        self._log(f"🌐 Language changed to: {langId}")
    
    @pyqtSlot(result=str)
    def getSavedLanguage(self):
        """Get the saved language from settings."""
        settings = self._load_settings()
        return settings.get("language", "en")
    
    def _log(self, msg):
        """Add debug log entry."""
        import datetime
        ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = f"[{ts}] {msg}"
        self._debug_logs.append(entry)
        # Keep last 500 entries
        if len(self._debug_logs) > 500:
            self._debug_logs = self._debug_logs[-500:]
        self.debugLog.emit(entry)
    
    def _emit_session_info(self):
        """Emit session info for nerd mode display."""
        info = {
            "has_session": self._session is not None,
            "cookie_preview": "",
            "base_url": "https://chatgpt.com/backend-api",
        }
        if self._session:
            cookie = self._session.cookies.get("__Secure-next-auth.session-token", "")
            if cookie:
                info["cookie_preview"] = cookie[:20] + "..." + cookie[-10:] if len(cookie) > 30 else cookie
            info["headers"] = dict(self._session.headers) if hasattr(self._session, 'headers') else {}
        self.sessionInfoChanged.emit(json.dumps(info, indent=2))
    
    @pyqtSlot(result=str)
    def getDebugLogs(self):
        """Get all debug logs as a string."""
        return "\n".join(self._debug_logs)
    
    @pyqtSlot()
    def clearDebugLogs(self):
        """Clear debug logs."""
        self._debug_logs = []
        self._log("Logs cleared")
    
    @pyqtSlot()
    def loadTasks(self):
        """Load tasks from API."""
        import time
        
        if not self._session:
            self._init_session()
        
        if not self._session:
            self.errorOccurred.emit("No session configured. Set up .env file.")
            self._log("❌ No session configured")
            return
        
        try:
            from ...codex.codex_tasks_list import tasks_list
            from ...etc.task_aliases import update_aliases
            
            self._log("→ GET /wham/tasks")
            start = time.time()
            tasks = tasks_list(self._session)
            elapsed = (time.time() - start) * 1000
            
            if tasks:
                update_aliases(tasks)
                self._task_model.set_tasks(tasks)
                self.statusMessage.emit(f"Loaded {len(tasks)} tasks")
                self._log(f"← {len(tasks)} tasks ({elapsed:.0f}ms)")
            else:
                self.statusMessage.emit("No tasks found")
                self._log(f"← 0 tasks ({elapsed:.0f}ms)")
            self.tasksLoaded.emit()
        except Exception as e:
            self.errorOccurred.emit(f"Failed to load tasks: {e}")
            self._log(f"❌ Failed: {e}")
    
    @pyqtSlot(int)
    def loadTaskDetail(self, index):
        """Load detail for task at index."""
        import time
        
        task = self._task_model.get_task(index)
        if not task:
            return
        
        try:
            from ...codex.codex_task_detail import task_detail
            
            task_id = task.get("id")
            self._log(f"→ GET /wham/tasks/{task_id[:8]}...")
            start = time.time()
            detail = task_detail(self._session, task_id)
            elapsed = (time.time() - start) * 1000
            
            self._current_task = detail
            self.taskDetailLoaded.emit(json.dumps(detail, indent=2, default=str))
            self._log(f"← Task detail ({elapsed:.0f}ms)")
        except Exception as e:
            self.errorOccurred.emit(f"Failed to load task: {e}")
            self._log(f"❌ Failed: {e}")
    
    @pyqtSlot(int)
    def archiveTask(self, index):
        """Archive task at index."""
        task = self._task_model.get_task(index)
        if not task:
            return
        
        try:
            from ...codex.codex_archive import archive_task
            
            task_id = task.get("id")
            result = archive_task(self._session, task_id)
            if result.get("success"):
                self.statusMessage.emit(f"Archived task #{index + 1}")
                self.loadTasks()  # Refresh
            else:
                self.errorOccurred.emit("Archive failed")
        except Exception as e:
            self.errorOccurred.emit(f"Archive failed: {e}")
    
    @pyqtSlot(int)
    def createPR(self, index):
        """Create PR for task at index."""
        task = self._task_model.get_task(index)
        if not task:
            return
        
        try:
            from ...codex.codex_turns import get_turns
            from ...codex.codex_create_pr import create_pr_for_turn
            
            task_id = task.get("id")
            turns_data = get_turns(self._session, task_id)
            current_turn_id = turns_data.get("current_turn_id")
            
            if current_turn_id:
                result = create_pr_for_turn(self._session, task_id, current_turn_id)
                pr_url = result.get("pull_request", {}).get("url", "")
                if pr_url:
                    self.statusMessage.emit(f"PR created: {pr_url}")
                else:
                    self.statusMessage.emit("PR created")
            else:
                self.errorOccurred.emit("No turn found for PR")
        except Exception as e:
            self.errorOccurred.emit(f"PR creation failed: {e}")
    
    @pyqtSlot(int)
    def extractPatch(self, index):
        """Extract patch for task at index."""
        task = self._task_model.get_task(index)
        if not task:
            return
        
        try:
            from ...codex.codex_turns import get_turns
            
            task_id = task.get("id")
            turns_data = get_turns(self._session, task_id)
            
            # Find diff in turns
            for turn_id, turn_data in turns_data.get("turn_mapping", {}).items():
                turn = turn_data.get("turn", {})
                for item in turn.get("output_items", []):
                    if "output_diff" in item:
                        diff = item["output_diff"].get("diff", "")
                        if diff:
                            self.patchReady.emit(diff)
                            return
            
            self.errorOccurred.emit("No patch found in task")
        except Exception as e:
            self.errorOccurred.emit(f"Patch extraction failed: {e}")
    
    @pyqtSlot(bool)
    def setPolling(self, enabled):
        """Enable/disable auto-refresh."""
        if enabled:
            self._poll_timer.start(30000)  # 30 seconds
            self.statusMessage.emit("Auto-refresh enabled (30s)")
        else:
            self._poll_timer.stop()
            self.statusMessage.emit("Auto-refresh disabled")
    
    @pyqtSlot()
    def openCodexBrowser(self):
        """Open Codex in system browser for task creation."""
        import webbrowser
        webbrowser.open("https://chatgpt.com/codex/")
    
    @pyqtSlot()
    def loadEnvironments(self):
        """Load available environments for task creation."""
        if not self._session:
            self._init_session()
        
        if not self._session:
            self.promptError.emit("No session configured. Set up .env file.")
            return
        
        try:
            from ...codex.json_get import _json_get
            
            # Try recent environments first
            url = "https://chatgpt.com/backend-api/wham/environments/recent"
            envs = _json_get(self._session, url)
            
            if not envs:
                # Fallback to all environments
                url = "https://chatgpt.com/backend-api/wham/environments"
                envs = _json_get(self._session, url)
            
            if envs and isinstance(envs, list):
                self._environments = envs
                self._env_model.set_environments(envs)
                # Convert to QVariantList for QML
                env_list = [
                    {
                        "id": e.get("id") or e.get("environment_id", ""),
                        "name": e.get("name") or e.get("full_name", ""),
                        "full_name": e.get("full_name") or e.get("name", ""),
                    }
                    for e in envs
                ]
                self.environmentsLoaded.emit(env_list)
                self.statusMessage.emit(f"Loaded {len(envs)} environments")
            else:
                self.promptError.emit("No environments found. Connect a repository in Codex first.")
        except Exception as e:
            self.promptError.emit(f"Failed to load environments: {e}")
    
    @pyqtSlot(str, str, str, int)
    def sendPrompt(self, prompt, envId, branch, bestOf):
        """Create a new task with the given prompt."""
        import time
        
        if not self._session:
            self._init_session()
        
        if not self._session:
            self.promptError.emit("No session configured")
            self._log("❌ No session for sendPrompt")
            return
        
        if not prompt:
            self.promptError.emit("No prompt provided")
            return
        
        if not envId:
            self.promptError.emit("No environment selected")
            return
        
        try:
            from ...codex.codex_create_task import create_task
            
            self._log(f"→ POST /wham/tasks (env={envId[:8]}..., branch={branch})")
            self._log(f"  Prompt: {prompt[:50]}..." if len(prompt) > 50 else f"  Prompt: {prompt}")
            start = time.time()
            
            result = create_task(
                session=self._session,
                prompt=prompt,
                environment_id=envId,
                branch=branch or "main",
                best_of_n=bestOf or 1,
            )
            elapsed = (time.time() - start) * 1000
            
            if result:
                task_id = result.get("task_id") or result.get("id", "")
                self.promptSuccess.emit(task_id)
                self.statusMessage.emit(f"Task created: {task_id[:8]}...")
                self._log(f"← Task created: {task_id} ({elapsed:.0f}ms)")
                # Refresh task list after a short delay
                QTimer.singleShot(2000, self.loadTasks)
            else:
                self.promptError.emit("Failed to create task. Check authentication.")
                self._log(f"❌ No result from create_task ({elapsed:.0f}ms)")
        except Exception as e:
            self.promptError.emit(f"Failed to create task: {e}")
            self._log(f"❌ Exception: {e}")
    
    @pyqtSlot(str)
    def openUrl(self, url):
        """Open URL in system browser."""
        if url:
            import webbrowser
            webbrowser.open(url)
    
    @pyqtSlot(str)
    def copyToClipboard(self, text):
        """Copy text to clipboard."""
        try:
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.statusMessage.emit("Copied to clipboard")
        except Exception as e:
            self.errorOccurred.emit(f"Copy failed: {e}")
    
    def _poll_tasks(self):
        """Poll for task updates."""
        self.loadTasks()
    
    def _init_session(self):
        """Initialize session from .env."""
        try:
            from ...codex.codex_session import session_from_env
            self._session = session_from_env()
        except Exception:
            pass
