from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt


class Breadcrumb(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.layout)
        self.breadcrumbs = []

    def add_crumb(self, name):
        crumb = QLabel(name)
        self.breadcrumbs.append(crumb)

        if len(self.breadcrumbs) > 1:
            separator = QLabel(">")
            self.layout.addWidget(separator)

        self.layout.addWidget(crumb)
