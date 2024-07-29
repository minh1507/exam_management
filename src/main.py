"""
Main server configuration.
"""

import sys
import os
import importlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt, pyqtSlot, QThread, QMetaObject, Q_ARG
from components.view.login import LoginWindow
from extends.log import *

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, reload_callback):
        super().__init__()
        self.reload_callback = reload_callback

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"{event.src_path} has been modified")
            self.reload_callback(event.src_path)



class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def showHome(self):
        self.stacked_widget.setCurrentWidget(self.home)

    def showSubject(self):
        self.stacked_widget.setCurrentWidget(self.subject)

    def showPermission(self):
        self.stacked_widget.setCurrentWidget(self.permission)

    def showAccount(self):
        self.stacked_widget.setCurrentWidget(self.account)

    def initUI(self):
        self.setWindowTitle('Exam Management')
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

        # Header
        header_widget = header(self)

        # Body
        body_widget = body(self)

        # Tool bar
        tool_bar_widget = tool_bar(self, body_widget["action"])

        self.main_layout.addWidget(header_widget)
        self.main_layout.addWidget(tool_bar_widget)
        self.main_layout.addWidget(body_widget["main"])


class WatcherThread(QThread):
    def __init__(self, folder_to_watch, reload_callback):
        super().__init__()
        self.folder_to_watch = folder_to_watch
        self.reload_callback = reload_callback

    def run(self):
        event_handler = ReloadHandler(self.reload_callback)
        observer = Observer()
        observer.schedule(event_handler, self.folder_to_watch, recursive=True)
        observer.start()
        observer.join()


def reload_module(file_path):
    module_name = os.path.relpath(file_path,
                                  './src').replace('/',
                                                   '.').replace('\\',
                                                                '.').rstrip('.py')
    try:
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
        else:
            importlib.import_module(module_name)
        QMetaObject.invokeMethod(
            window,
            "load_ui_components",
            Qt.QueuedConnection)
    except Exception as e:
        print(f"Failed to reload module: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        window = FullScreenWindow()
        window.show()

        if './src' not in sys.path:
            sys.path.append('./src')

        watcher_thread = WatcherThread("./src", reload_module)
        watcher_thread.start()

        try:
            sys.exit(app.exec_())
        except KeyboardInterrupt:
            watcher_thread.terminate()
            watcher_thread.wait()
