"""Main entry point for PyQt6 UI."""
import sys
import os
from pathlib import Path


def launch(session=None):
    """Launch the PyQt6 desktop UI."""
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtQml import QQmlApplicationEngine
        from PyQt6.QtCore import QUrl
    except ImportError:
        print("PyQt6 not installed. Install with:")
        print("  pip install PyQt6 PyQt6-WebEngine")
        return 1
    
    from .controllers.app_controller import AppController
    
    app = QApplication(sys.argv)
    app.setApplicationName("Codex Task Runner")
    app.setOrganizationName("codex-task-runner")
    
    engine = QQmlApplicationEngine()
    
    # Create controller and keep reference
    controller = AppController(session)
    
    # Register before loading QML
    engine.rootContext().setContextProperty("app", controller)
    
    # Load QML
    qml_path = Path(__file__).parent / "qml" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    
    if not engine.rootObjects():
        print("Failed to load QML")
        return 1
    
    # Keep controller alive
    engine.rootObjects()[0].setProperty("controller", controller)
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(launch())
