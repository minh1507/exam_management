from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QTableWidgetItem, QTableWidget, QFrame,
    QPushButton, QDialog, QDialogButtonBox, QLineEdit, QFormLayout, QMessageBox, QHBoxLayout, QHeaderView
)
from PyQt5.QtCore import Qt
from ..layout.breadcrumb import Breadcrumb

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(project_root)

from src.services.subject import SubjectService

class CreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Create Row')
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        self.order_input = QLineEdit(self)
        self.code_input = QLineEdit(self)
        self.name_input = QLineEdit(self)
        layout.addRow('Order', self.order_input)
        layout.addRow('Code', self.code_input)
        layout.addRow('Name', self.name_input)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_data(self):
        return [
            self.order_input.text(),
            self.code_input.text(),
            self.name_input.text()
        ]

class UpdateDialog(QDialog):
    def __init__(self, row_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Update Row')
        self.row_data = row_data
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        self.order_input = QLineEdit(str(self.row_data[1]), self)  
        self.code_input = QLineEdit(self.row_data[2], self)       
        self.name_input = QLineEdit(self.row_data[3], self)       
        layout.addRow('Order', self.order_input)
        layout.addRow('Code', self.code_input)
        layout.addRow('Name', self.name_input)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_data(self):
        return [
            self.order_input.text(),
            self.code_input.text(),
            self.name_input.text()
        ]

class DeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Delete Row')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel('Are you sure you want to delete this row?', self)
        layout.addWidget(label)
        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

class Subject(QWidget):
    def __init__(self):
        super().__init__()
        self.subject_service = SubjectService()  
        self.data = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignTop)
        breadcrumb = Breadcrumb()
        breadcrumb.add_crumb("Home")
        breadcrumb.add_crumb("Category")
        breadcrumb.add_crumb("Subject")
        content_layout.addWidget(breadcrumb)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        content_layout.addWidget(line)
        create_button = QPushButton('Create')
        create_button.setFixedWidth(100)
        create_button.clicked.connect(self.open_create_dialog)
        content_layout.addWidget(create_button)
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['Id', 'Order', 'Code', 'Name', 'Action'])
        content_layout.addWidget(self.table_widget)
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        self.get()

    def open_create_dialog(self):
        dialog = CreateDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_data = dialog.get_data()
            error = self.subject_service.create_subject(new_data)
            if error:
                QMessageBox.critical(self, 'Database Error', error)
            else:
                self.get()

    def open_update_dialog(self, row):
        dialog = UpdateDialog(self.data[row], self)
        if dialog.exec_() == QDialog.Accepted:
            new_data = dialog.get_data()
            error = self.subject_service.update_subject(self.data[row][0], new_data)
            if error:
                QMessageBox.critical(self, 'Database Error', error)
            else:
                self.get()

    def open_delete_dialog(self, row):
        dialog = DeleteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            error = self.subject_service.delete_subject(self.data[row][0])
            if error:
                QMessageBox.critical(self, 'Database Error', error)
            else:
                self.get()

    def get(self):
        data, error = self.subject_service.fetch_subjects()
        if error:
            QMessageBox.critical(self, 'Database Error', error)
            self.data = []
        else:
            self.data = data
            self.table_widget.setRowCount(len(self.data))
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for row_index, row_data in enumerate(self.data):
                for col_index, item in enumerate(row_data):
                    self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(item)))
                action_widget = QWidget()
                action_layout = QHBoxLayout()
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setSpacing(10)
                update_button = QPushButton('Update')
                delete_button = QPushButton('Delete')
                update_button.setFixedWidth(100)
                delete_button.setFixedWidth(100)
                action_layout.addWidget(update_button)
                action_layout.addWidget(delete_button)
                action_layout.addStretch()
                action_widget.setLayout(action_layout)
                update_button.clicked.connect(self.make_update_callback(row_index))
                delete_button.clicked.connect(self.make_delete_callback(row_index))
                self.table_widget.setCellWidget(row_index, 4, action_widget)


    def make_update_callback(self, row_index):
        return lambda: self.open_update_dialog(row_index)

    def make_delete_callback(self, row_index):
        return lambda: self.open_delete_dialog(row_index)
