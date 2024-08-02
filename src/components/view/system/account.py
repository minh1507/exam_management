from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QDialog,
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QHBoxLayout,
    QComboBox
)
from PyQt5.QtCore import Qt
import sys
import os
from ..base import ScrollableWidget

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"))
sys.path.append(project_root)
from src.services.account import AccountService
from src.services.role import RoleService
from src.common.i18n.lang import Trans

class CreateDialog(QDialog):
    def __init__(self, roles, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Create Account')
        self.roles = roles
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText(self.parent.trans.objectT("username"))
        self.username_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Username'), self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText(self.parent.trans.objectT("password"))
        self.password_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Password'), self.password_input)

        self.role_input = QComboBox(self)
        self.role_input.addItems(self.roles)
        self.role_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Role'), self.role_input)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-size: 12px;")
        self.error_label.setWordWrap(True)
        self.error_label.setVisible(False)
        form_layout.addRow(self.error_label)

        submit_button = QPushButton(self.parent.trans.actionT("submit"), self)
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        submit_button.clicked.connect(self.accept)

        cancel_button = QPushButton(self.parent.trans.actionT("cancel"), self)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6f61;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff4b3a;
            }
            QPushButton:pressed {
                background-color: #e03a1e;
            }
        """)
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)
        button_layout.setStretch(0, 1)
        button_layout.setStretch(1, 1)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.setContentsMargins(20, 20, 20, 20) 

        self.setMinimumSize(350, 250)

    def set_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def get_data(self):
        return [
            self.username_input.text(),
            self.password_input.text(),
            self.role_input.currentText()
        ]

class DeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Delete Row')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Message Label
        message_label = QLabel('Are you sure you want to delete this row?', self)
        message_label.setStyleSheet("font-size: 16px; padding: 20px;")
        layout.addWidget(message_label)

        yes_button = QPushButton('Yes', self)
        yes_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        yes_button.clicked.connect(self.accept)

        no_button = QPushButton('No', self)
        no_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        no_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)
        button_layout.setStretch(0, 1)
        button_layout.setStretch(1, 1)

        layout.addLayout(button_layout)
        layout.setContentsMargins(20, 20, 20, 20) 

        self.setMinimumSize(300, 150)

class Account(ScrollableWidget):
    breadcrumbs = ["Home", "System", "Account"]

    def __init__(self):
        super().__init__()
        self.account_service = AccountService()
        self.data = []
        self.roles = RoleService()
        self.trans = Trans()
        self.init_ui()

    def init_ui(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.content_layout.addWidget(line)

        create_button = QPushButton(self.trans.buttonT("create"))
        create_button.setFixedSize(100, 30)  
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff !important;
                font-weight: bold;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;  
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3; 
            }
            QPushButton:pressed {
                background-color: #004085; 
            }
        """)
        create_button.clicked.connect(self.open_create_dialog)
        self.content_layout.addWidget(create_button)

        self.cards_layout = QVBoxLayout()
        self.cards_layout.setContentsMargins(0, 0, 0, 0)  
        self.cards_layout.setSpacing(10) 
        self.content_layout.addLayout(self.cards_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.get()

    def open_create_dialog(self):
        roles = self.roles.fetch_roles()
        dialog = CreateDialog([role['name'] for role in roles], self)
        
        while True:
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_data()

                for i in roles:
                    if i['name'] == new_data[-1]:
                        new_data[-1] = i["id"]

                response = self.account_service.create_account(new_data)
                if response.get("status") == 400:
                    dialog.set_error(self.trans.message(response["messages"][0]))
                    continue  
                else:
                    self.get()
                    break 
            else:
                break

    def get(self):
        data = self.account_service.fetch_account()
        self.data = data
        self.clear_cards()

        for account in self.data:
            self.create_card(account)

    def clear_cards(self):
        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def create_card(self, account):
        card = QFrame()
        card.setFrameShape(QFrame.NoFrame)
        card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(0, 0, 0, 0)  
        card_layout.setSpacing(5)  

        name_label = QLabel(f"{account['username']}")
        name_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        """)

        lastname_label = QLabel(f"Name: {account['profiling']["lastname"]}")
        lastname_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
            margin-bottom: 0 !important;    
            padding-bottom: 0 !important;    
        """)

        role_label = QLabel(f"Role: {account['role']['name']}")
        role_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)

        card_layout.addWidget(name_label)
        card_layout.addWidget(lastname_label)
        card_layout.addWidget(role_label)

        action_widget = QWidget()
        action_layout = QHBoxLayout()
        action_layout.setContentsMargins(5, 5, 5, 5)
        action_layout.setSpacing(10)
        action_layout.setAlignment(Qt.AlignLeft)

        delete_button = QPushButton(self.trans.buttonT("delete"))
        delete_button.setFixedWidth(100)
        delete_button.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #ff6f61;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff4b3a;
            }
            QPushButton:pressed {
                background-color: #e03a1e;
            }
        """)
        action_layout.addWidget(delete_button)
        action_widget.setLayout(action_layout)
        card_layout.addWidget(action_widget)

        delete_button.clicked.connect(
            self.make_delete_callback(account['id']))

        card.setLayout(card_layout)
        self.cards_layout.addWidget(card)

    def make_delete_callback(self, account_id):
        return lambda: self.open_delete_dialog(account_id)

    def open_delete_dialog(self, account_id):
        dialog = DeleteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            response = self.account_service.delete_account(account_id)
            if response["status"] == 200:  
                self.get()  
            else:
                QMessageBox.critical(self, "Error", "Failed to delete the account.")
