from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class Breadcrumb(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.setLayout(self.layout)
        self.breadcrumbs = []

    def add_crumb(self, name, callback=None):
        # Create a label for the breadcrumb item
        crumb = QLabel(name)
        self.layout.addWidget(crumb)

        if callback:
            crumb = QPushButton(name)
            crumb.clicked.connect(callback)
            self.layout.addWidget(crumb)
        else:
            crumb = QLabel(name)
            self.layout.addWidget(crumb)

        self.breadcrumbs.append(crumb)
        
        # Add separator if it's not the first breadcrumb
        if len(self.breadcrumbs) > 1:
            separator = QLabel(">")
            self.layout.insertWidget(self.layout.count() - 1, separator)

