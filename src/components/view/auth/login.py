from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"))
sys.path.append(project_root)
from src.services.login import LoginService
from src.commons.hashing import HashingUltil
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.login_service = LoginService()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setFixedSize(400, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
                background-color: #0078d4;
                color: white;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
        """)

        layout = QVBoxLayout()

        logo = QLabel(self)
        logo.setText("Exam management")
        logo.setFont(QFont("Arial", 16, QFont.Bold))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.invalid_label = QLabel("Invalid credentials", self)
        self.invalid_label.setStyleSheet("color: red;")
        self.invalid_label.hide()
        layout.addWidget(self.invalid_label)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def off(self):
        self.invalid_label.show()

    def check_login(self):
        data, error = self.login_service.fetch_one(self.username_input.text())
        if data is None:
            self.off()
        else:
            if HashingUltil.compare(data[-1], self.password_input.text()) == True:
                self.accept()
            else: 
                self.off()