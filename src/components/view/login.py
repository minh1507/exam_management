from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
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

    def check_login(self):
        if (self.username_input.text() == 'admin' and
                self.password_input.text() == 'password'):
            self.accept()
        else:
            self.invalid_label.show()
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()
