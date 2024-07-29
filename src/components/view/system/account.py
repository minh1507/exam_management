from PyQt5.QtWidgets import QLabel
from ..base import ScrollableWidget
class Account(ScrollableWidget):
    def __init__(self):
        super().__init__()

        header = QLabel("Account")
        header.setStyleSheet("font-size: 24px; padding: 10px;")

        self.content_layout.addWidget(header)
