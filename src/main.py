import sys
import os
import importlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt, QThread, QMetaObject, pyqtSlot
from components.view.auth.login import LoginWindow
from extends.log import *
from common.i18n.lang import Trans

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = None
        self.login_window = None
        self.watcher_thread = None
        self.trans = Trans()

    class ReloadHandler(FileSystemEventHandler):
        def __init__(self, reload_callback):
            super().__init__()
            self.reload_callback = reload_callback

        def on_modified(self, event):
            if event.src_path.endswith(".py"):
                print(f"{event.src_path} has been modified")
                self.reload_callback(event.src_path)

    class WatcherThread(QThread):
        def __init__(self, folder_to_watch, reload_callback):
            super().__init__()
            self.folder_to_watch = folder_to_watch
            self.reload_callback = reload_callback

        def run(self):
            event_handler = Application.ReloadHandler(self.reload_callback)
            observer = Observer()
            observer.schedule(event_handler, self.folder_to_watch, recursive=True)
            observer.start()
            observer.join()

    def reload_module(self, file_path):
        module_name = os.path.relpath(file_path, './src').replace('/', '.').replace('\\', '.').rstrip('.py')
        try:
            if module_name in sys.modules:
                importlib.reload(sys.modules[module_name])
            else:
                importlib.import_module(module_name)
            QMetaObject.invokeMethod(self.window, "load_ui_components", Qt.QueuedConnection)
        except Exception as e:
            print(f"Failed to reload module: {e}")

    def show_full_screen_window(self):
        class FullScreenWindow(QMainWindow):
            def __init__(self, app):
                super().__init__()
                if not isinstance(app.login_window, QDialog):
                    raise TypeError("login_window must be a QDialog instance")
                self.app = app
                self.initUI()

            def initUI(self):
                self.setWindowTitle(self.app.trans.objectT("exam_management"))
                self.showFullScreen()
                central_widget = QWidget()
                self.setCentralWidget(central_widget)
                self.main_layout = QVBoxLayout(central_widget)
                self.main_layout.setAlignment(Qt.AlignTop)
                self.main_layout.setContentsMargins(0, 0, 0, 0)
                self.main_layout.setSpacing(0)

                self.load_ui_components()

            @pyqtSlot()
            def load_ui_components(self):
                from components.layout.header import header
                from components.layout.tool_bar import tool_bar
                from components.layout.body import body

                for i in reversed(range(self.main_layout.count())):
                    widget = self.main_layout.itemAt(i).widget()
                    if widget is not None:
                        widget.setParent(None)

                header_widget = header(self)
                body_widget = body(self)
                tool_bar_widget = tool_bar(self, body_widget["action"], self.app.login_window)

                self.main_layout.addWidget(header_widget)
                self.main_layout.addWidget(tool_bar_widget)
                self.main_layout.addWidget(body_widget["main"])

        self.window = FullScreenWindow(self)
        self.window.show()

    def start(self):
        while True:
            try:
                self.login_window = LoginWindow(self)
                self.login_window.show()

                result = self.login_window.exec_()

                if result == QDialog.Accepted:
                    if './src' not in sys.path:
                        sys.path.append('./src')

                    self.watcher_thread = self.WatcherThread("./src", self.reload_module)
                    self.watcher_thread.start()

                    try:
                        print("Entering application event loop...")
                        self.app.exec_()
                        print("Exited application event loop.")
                    except Exception as e:
                        print(f"Exception during application event loop: {e}")
                    finally:
                        self.watcher_thread.terminate()
                        self.watcher_thread.wait()
                    break
                else:
                    print("Login failed or dialog was canceled.")
                    break
            except Exception as e:
                print(f"Unhandled exception: {e}")
                break

if __name__ == '__main__':
    app = Application()
    app.start()
