from PyQt5.QtWidgets import (
    QWidget,
    QTableWidgetItem,
    QTableWidget,
    QFrame,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    )
from PyQt5.QtCore import Qt
from ..base import ScrollableWidget

import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"))
sys.path.append(project_root)
from src.services.role import RoleService

class Role(ScrollableWidget):
    breadcrumbs = ["Home", "System", "Role"]

    def __init__(self):
        super().__init__()
        self.role_service = RoleService()
        self.data = []
        self.init_ui()

    def init_ui(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.content_layout.addWidget(line)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Id', 'Name', 'Code'])
        self.content_layout.addWidget(self.table_widget)


    def showEvent(self, event):
        super().showEvent(event)
        self.get()

    def get(self):
        data = self.role_service.fetch_roles()
        self.data = data

        if not self.data:
            return

        num_columns = self.table_widget.columnCount()
        self.table_widget.setRowCount(len(self.data))

        for row_index, row_data in enumerate(self.data):
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(row_data['id']))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(row_data['name']))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(row_data['code']))



            