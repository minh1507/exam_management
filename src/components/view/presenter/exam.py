from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QDialog,
    QLineEdit,
    QDateTimeEdit,
    QFormLayout,
    QHBoxLayout,
    QComboBox
)
from PyQt5.QtCore import Qt
import sys
import os
from ..base import ScrollableWidget
from PyQt5.QtGui import QIcon
project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"))
sys.path.append(project_root)
from src.services.subject import SubjectService
from src.services.exam import ExamService
from src.common.i18n.lang import Trans

class CreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Create Subject')
        self.setWindowIcon(QIcon("src/assets/icon/create.png"))
        self.parent = parent
        self.subjectService = SubjectService()
        self.init_ui()

    def init_ui(self):
        self.subjects = self.subjectService.fetch_subjects()

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText(self.parent.trans.objectT("code"))
        self.code_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Code'), self.code_input)

        self.supervisor_input = QLineEdit(self)
        self.supervisor_input.setPlaceholderText(self.parent.trans.objectT("supervisor"))
        self.supervisor_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Supervisor'), self.supervisor_input)

        self.total_question_input = QLineEdit(self)
        self.total_question_input.setPlaceholderText(self.parent.trans.objectT("number_of_question"))
        self.total_question_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Number of question'), self.total_question_input)

        self.expired_time_input = QDateTimeEdit(self)
        self.expired_time_input.setStyleSheet("padding: 10px;")
        form_layout.addRow(QLabel('Expired time'), self.expired_time_input)

        self.start_time_input = QDateTimeEdit(self)
        self.start_time_input.setStyleSheet("padding: 10px;")
        form_layout.addRow(QLabel('Start time'), self.start_time_input)

        self.subject_input = QComboBox(self)
        self.subject_input.addItems([subject['name'] for subject in self.subjects])
        self.subject_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Subject'), self.subject_input)

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

        self.setMinimumSize(500, 250)

    def set_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def get_data(self):
        return {
            'supervisor': self.supervisor_input.text(),
            'code': self.code_input.text(),
            'start_time': self.start_time_input.date().toPyDate().strftime("%Y-%m-%d"),
            'expired_time': self.expired_time_input.date().toPyDate().strftime("%Y-%m-%d"),
            "total_question": self.total_question_input.text(),
            'subject': next((subject['id'] for subject in self.subjects if subject['name'] == self.subject_input.currentText()), None),
        }

class DeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Delete subject')
        self.setWindowIcon(QIcon("src/assets/icon/delete.png"))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

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

class UpdateDialog(QDialog):
    def __init__(self, subject, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Update Subject')
        self.setWindowIcon(QIcon("src/assets/icon/update.png"))
        self.subject = subject
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.order_input = QLineEdit(self)
        self.order_input.setText(str(self.subject['order']))
        self.order_input.setPlaceholderText(self.parent.trans.objectT("order"))
        self.order_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Order'), self.order_input)

        self.code_input = QLineEdit(self)
        self.code_input.setText(self.subject['code'])
        self.code_input.setPlaceholderText(self.parent.trans.objectT("code"))
        self.code_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Code'), self.code_input)

        self.name_input = QLineEdit(self)
        self.name_input.setText(self.subject['name'])
        self.name_input.setPlaceholderText(self.parent.trans.objectT("name"))
        self.name_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Name'), self.name_input)

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
        return {
            'order': self.order_input.text(),
            'code': self.code_input.text(),
            'name': self.name_input.text()
        }

class Exam(ScrollableWidget):
    breadcrumbs = ["Home", "Presenter", "Exam"]

    def __init__(self):
        super().__init__()
        self.exam_service = ExamService()
        self.data = []
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
        dialog = CreateDialog(self)
        
        while True:
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_data()
                response = self.exam_service.create_exam(new_data)
                if response['status'] == 400:
                    dialog.set_error(self.trans.message(response["messages"][0]))
                    continue
                else:
                    self.get()
                    break
            else:
                break

    def get(self):
        data = self.exam_service.fetch_exams()
        self.data = data
        self.clear_cards()

        for exam in self.data:
            self.create_card(exam)

    def clear_cards(self):
        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def create_card(self, exam):
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

        code_label = QLabel(f"{exam['code']}")
        code_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        """)

        subject_label = QLabel(f"Subject: {exam['subject']['name']}")
        subject_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)

        supervisor_label = QLabel(f"Supervisor: {exam['supervisor']}")
        supervisor_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)

        expired_time_label = QLabel(f"Time expired: {exam['expired_time']}")
        expired_time_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)

        start_time_label = QLabel(f"Time start: {exam['start_time']}")
        start_time_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)

        total_question_label = QLabel(f"Number of question: {exam['total_question']}")
        total_question_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)

        card_layout.addWidget(code_label)
        card_layout.addWidget(subject_label)
        card_layout.addWidget(supervisor_label)
        card_layout.addWidget(expired_time_label)
        card_layout.addWidget(start_time_label)
        card_layout.addWidget(total_question_label)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignLeft)

        delete_button = QPushButton("Delete")
        delete_button.setFixedWidth(100)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        delete_button.clicked.connect(lambda: self.delete(exam['id']))

        button_layout.addWidget(delete_button)

        card_layout.addLayout(button_layout)

        card.setLayout(card_layout)
        
        self.cards_layout.addWidget(card)


    def delete(self, exam_id):
        dialog = DeleteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.exam_service.delete_exam(exam_id)
            self.get()

    def update(self, exam):
        dialog = UpdateDialog(exam, self)
        while True:
            if dialog.exec_() == QDialog.Accepted:
                updated_data = dialog.get_data()
                response = self.exam_service.update_exam(exam['id'], updated_data)
                if response['status'] == 400:
                    dialog.set_error(self.trans.message(response["messages"][0]))
                    continue
                else:
                    self.get()
                    break
            else:
                break
