from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt


def header(self):
    header_widget = QWidget()
    header_layout = QHBoxLayout(header_widget)

    header_layout.setContentsMargins(10, 0, 10, 0)
    header_widget.setStyleSheet("""
        background-color: #2c3e50;
        border-bottom: 2px solid #34495e;
        padding: 10px
    """)
    header_widget.setFixedHeight(50)

    title_label = QLabel(self.trans.objectT("exam_management"), self)
    title_label.setStyleSheet("""
        color: white;
    """)
    title_label.setAlignment(Qt.AlignCenter)

    exit_button = QPushButton('✖', self)
    exit_button.setFixedSize(30, 30)
    exit_button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
            color: white;
            font-weight: bold;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
    exit_button.clicked.connect(self.close)

    header_layout.addWidget(title_label)
    header_layout.addWidget(exit_button)
    return header_widget
