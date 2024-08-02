from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import jwt
import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"))
sys.path.append(project_root)
from src.services.login import LoginService
from src.common.static.global_c import Global
from src.common.i18n.lang import Trans

class LoginWindow(QDialog):
    def __init__(self, on_login_success):
        super().__init__()
        self.login_service = LoginService()
        self.on_login_success = on_login_success
        self.trans = Trans()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.trans.objectT("login"))
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
        logo.setText(self.trans.objectT("exam_management"))
        logo.setFont(QFont("Arial", 16, QFont.Bold))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText(self.trans.objectT("username"))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText(self.trans.objectT("password"))
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.invalid_label = QLabel("", self)
        self.invalid_label.setStyleSheet("color: red;")
        self.invalid_label.hide()
        layout.addWidget(self.invalid_label)

        self.login_button = QPushButton(self.trans.objectT("login"), self)
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def off(self):
        self.invalid_label.show()
    
    def on(self):
        self.invalid_label.hide()

    def check_login(self):
        response = self.login_service.login(self.username_input.text(), self.password_input.text())

        if(response["status"] == 400):
            self.invalid_label.setText(self.trans.message(response["messages"][0]))
            self.off()
        else:
            Global.token = response["data"]["accessToken"]
            Global.data = jwt.decode(Global.token, "123", algorithms=['HS256'])
            self.on()
            self.accept()  
            self.on_login_success()
