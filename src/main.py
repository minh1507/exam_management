import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from components.layout.header import header
from components.layout.tool_bar import tool_bar
from components.layout.body import body
from PyQt5.QtCore import Qt

class FullScreenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def showHome(self):
        self.stacked_widget.setCurrentWidget(self.home)

    def showView2(self):
        self.stacked_widget.setCurrentWidget(self.view2)

    def initUI(self):
        self.setWindowTitle('Exam Management')
        self.showFullScreen()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header_widget = header(self)

        # Body
        body_widget = body(self)
     
        # Tool bar
        tool_bar_widget = tool_bar(self, body_widget["action"])

        main_layout.addWidget(header_widget)
        main_layout.addWidget(tool_bar_widget)
        main_layout.addWidget(body_widget["main"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    sys.exit(app.exec_())