from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidgetItem,
    QTableWidget,
    QFrame,
    QPushButton,
    QDialog,
    QDialogButtonBox,
    QLineEdit,
    QFormLayout,
    QMessageBox,
    QHBoxLayout,
    QHeaderView,
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

class CreateDialog(QDialog):
    def __init__(self, roles, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Create Row')
        self.roles = roles
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.role_input = QComboBox(self)
        self.role_input.addItems(self.roles)
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setWordWrap(True)
        self.error_label.setVisible(False)  
        layout.addRow('Username', self.username_input)
        layout.addRow('Password', self.password_input)
        layout.addRow('Role', self.role_input)
        layout.addRow(self.error_label)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def set_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True) 

    def get_data(self):
        return [
            self.username_input.text(),
            self.password_input.text(),
            self.role_input.currentText()
        ]

class Account(ScrollableWidget):
    breadcrumbs = ["Home", "System", "Account"]

    def __init__(self):
        super().__init__()
        self.account_service = AccountService()
        self.data = []
        self.roles = RoleService()
        self.init_ui()

    def init_ui(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.content_layout.addWidget(line)

        create_button = QPushButton('Create')
        create_button.setFixedWidth(100)
        create_button.clicked.connect(self.open_create_dialog)
        self.content_layout.addWidget(create_button)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(
            ['Id', 'Username', 'Role', 'Action'])
        self.content_layout.addWidget(self.table_widget)

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
                    dialog.set_error("Error creating account. Please check the provided information.")
                    continue  
                else:
                    self.get()
                    break 
            else:
                break

    def get(self):
        data = self.account_service.fetch_account()
        self.data = data
        self.table_widget.setRowCount(len(self.data))
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        for row_index, row_data in enumerate(self.data):
            id_ = row_data['id']
            username = row_data['username']
            role_name = row_data['role']['name']
            items = [id_, username, role_name]

            for col_index, item in enumerate(items):
                table_item = QTableWidgetItem(str(item))
                table_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.table_widget.setItem(row_index, col_index, table_item)

            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(5, 5, 5, 5)
            action_layout.setSpacing(10)
            action_layout.setAlignment(Qt.AlignLeft)
            delete_button = QPushButton('Delete')
            delete_button.setFixedWidth(100)
            action_layout.addWidget(delete_button)
            action_widget.setLayout(action_layout)
            delete_button.clicked.connect(
                self.make_delete_callback(row_index))
            self.table_widget.setCellWidget(row_index, 3, action_widget)

    def make_update_callback(self, row_index):
        return lambda: self.open_update_dialog(row_index)

    def make_delete_callback(self, row_index):
        return lambda: self.open_delete_dialog(row_index)

    def open_delete_dialog(self, row):
        dialog = DeleteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            error = self.account_service.delete_subject(self.data[row][0])
            if error:
                QMessageBox.critical(self, 'Database Error', error)
            else:
                self.get()
