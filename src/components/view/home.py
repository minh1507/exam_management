from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt

class Home(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignTop)

        header = QLabel("Exam list")
        header.setStyleSheet("font-size: 24px; padding: 10px;")

        content_layout.addWidget(header)

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)

        layout.addWidget(scroll_area)
        self.setLayout(layout)



