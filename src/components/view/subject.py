from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class Subject(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is View 2"))
        self.setLayout(layout)
