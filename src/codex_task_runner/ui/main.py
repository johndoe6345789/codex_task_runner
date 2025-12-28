"""Main entry point for PyQt6 UI."""
import sys
import os
from pathlib import Path

# Keep controller reference alive
_controller = None


def launch(session=None):
    """Launch the PyQt6 desktop UI."""
    global _controller
    
    # macOS-specific Qt settings for proper rendering
    if sys.platform == 'darwin':
        # Use basic render loop for better compatibility
        os.environ.setdefault('QSG_RENDER_LOOP', 'basic')
        # Disable threaded rendering which can cause issues on macOS
        os.environ.setdefault('QSG_RHI_BACKEND', 'metal')
    
    # Force Basic style to allow full customization
    os.environ['QT_QUICK_CONTROLS_STYLE'] = 'Basic'
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtQml import QQmlApplicationEngine
        from PyQt6.QtCore import QUrl, Qt
        from PyQt6.QtQuick import QQuickWindow
    except ImportError:
        print("PyQt6 not installed. Install with:")
        print("  pip install PyQt6 PyQt6-WebEngine")
        return 1
    
    # Set high DPI attributes before creating QApplication
    if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    
    from .controllers.app_controller import AppController
    
    app = QApplication(sys.argv)
    app.setApplicationName("Codex Task Runner")
    app.setOrganizationName("codex-task-runner")
    
    # Create controller and keep global reference
    _controller = AppController(session)
    
    engine = QQmlApplicationEngine()
    
    # Handle QML errors
    def on_object_created(obj, url):
        if obj is None:
            print(f"Failed to create QML object from {url}")
    
    engine.objectCreated.connect(on_object_created)
    
    # Register before loading QML
    engine.rootContext().setContextProperty("app", _controller)
    
    # Add QML import path for components and fakemui
    qml_dir = Path(__file__).parent / "qml"
    engine.addImportPath(str(qml_dir))
    engine.addImportPath(str(qml_dir / "fakemui"))
    engine.addImportPath(str(qml_dir / "components"))
    engine.addImportPath(str(qml_dir / "contexts"))
    
    # Load QML - App.qml is the full-featured entry point
    qml_path = qml_dir / "App.qml"
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    
    if not engine.rootObjects():
        print("Failed to load QML - check for QML syntax errors")
        return 1
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(launch())
