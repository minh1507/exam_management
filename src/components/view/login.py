from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_login(self):
        # Simple username and password check; replace with actual authentication
        if (self.username_input.text() == 'admin' and
                self.password_input.text() == 'password'):
            self.accept()  # Close the login window and return QDialog.Accepted
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()
            # Optionally show an error message
            QLabel("Invalid credentials", self).show()
