from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
)
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

        self.cards_layout = QVBoxLayout()
        self.cards_layout.setContentsMargins(0, 0, 0, 0)  
        self.cards_layout.setSpacing(10)  
        self.content_layout.addLayout(self.cards_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.get()

    def get(self):
        data = self.role_service.fetch_roles()
        self.data = data

        if not self.data:
            return

        self.clear_cards()

        for role in self.data:
            self.create_card(role)

    def clear_cards(self):
        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def create_card(self, role):
        card = QFrame()
        card.setFrameShape(QFrame.NoFrame)
        card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            padding: 10px;
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(0, 0, 0, 0)  
        card_layout.setSpacing(5) 
        name_label = QLabel(f"{role['name']}")
        name_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        """)
        card_layout.addWidget(name_label)

        code_label = QLabel(f"Code: {role['code']}")
        code_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)

        card_layout.addWidget(code_label)

        card.setLayout(card_layout)
        self.cards_layout.addWidget(card)
