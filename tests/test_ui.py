"""Test PyQt6 UI launches and renders correctly."""
import sys
import os
from pathlib import Path

import pytest


@pytest.fixture
def app():
    """Create QApplication for tests."""
    from PyQt6.QtWidgets import QApplication
    # Ensure we have a fresh app or reuse existing
    existing = QApplication.instance()
    if existing:
        yield existing
    else:
        app = QApplication(sys.argv)
        yield app


def test_ui_launches_and_screenshots(app, tmp_path):
    """Test that UI launches, renders, and can be screenshotted."""
    from PyQt6.QtQml import QQmlApplicationEngine
    from PyQt6.QtCore import QUrl, QTimer
    
    from codex_task_runner.ui.controllers.app_controller import AppController
    
    # Create controller (no session needed for basic render test)
    controller = AppController(None)
    
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("app", controller)
    
    # Load QML
    qml_path = Path(__file__).parent.parent / "src" / "codex_task_runner" / "ui" / "qml" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    
    assert engine.rootObjects(), "QML failed to load"
    
    window = engine.rootObjects()[0]
    assert window is not None
    
    # Track test completion
    screenshot_taken = [False]
    screenshot_path = tmp_path / "ui_screenshot.png"
    
    def take_screenshot_and_close():
        try:
            # Use window's grab method instead of screen grab
            from PyQt6.QtQuick import QQuickWindow
            if isinstance(window, QQuickWindow):
                image = window.grabWindow()
                image.save(str(screenshot_path))
                screenshot_taken[0] = True
                print(f"Screenshot saved to: {screenshot_path}")
        except Exception as e:
            print(f"Screenshot failed: {e}")
        finally:
            # Close window
            window.close()
            app.quit()
    
    # Schedule screenshot after 1 second
    QTimer.singleShot(1000, take_screenshot_and_close)
    
    # Run event loop (will exit when window closes)
    app.exec()
    
    assert screenshot_taken[0], "Screenshot was not taken"
    assert screenshot_path.exists(), f"Screenshot file not found: {screenshot_path}"
    assert screenshot_path.stat().st_size > 0, "Screenshot file is empty"
    
    print(f"✓ UI test passed. Screenshot: {screenshot_path}")


if __name__ == "__main__":
    # Run standalone for manual testing
    from PyQt6.QtWidgets import QApplication
    
    # Avoid duplicate QApplication
    existing = QApplication.instance()
    app = existing if existing else QApplication(sys.argv)
    
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        test_ui_launches_and_screenshots(app, Path(tmp))
