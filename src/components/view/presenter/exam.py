from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QDialog,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QComboBox,
    QScrollArea,
    QWidget,
    QGroupBox,
)
from PyQt5.QtCore import Qt
import sys
import os
from ..base import ScrollableWidget
from PyQt5.QtGui import QIcon, QPixmap
project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"))
sys.path.append(project_root)
from src.services.subject import SubjectService
from src.services.exam import ExamService
from src.common.i18n.lang import Trans
import requests
from src.common.helper.string import StringHelper

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

        self.duration_input = QLineEdit(self)
        self.duration_input.setPlaceholderText("Duration")
        self.duration_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Duration'), self.duration_input)

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
            'duration': self.duration_input.text(),
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

class Detail(QDialog):
    def __init__(self, parent=None, questions=None):
        super().__init__(parent)
        self.setWindowTitle('Detail subject')
        self.setWindowIcon(QIcon("src/assets/icon/profile.png"))
        self.questions = questions
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        scroll_layout = QVBoxLayout(content_widget)
        scroll_layout.setSpacing(15)

        for question in self.questions:
            question_box = QGroupBox()
            question_box.setStyleSheet("""
                QGroupBox {
                    border: 1px solid #d3d3d3;
                    border-radius: 5px;
                    margin-top: 15px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top center;
                    padding: 0 3px;
                }
            """)
            question_layout = QVBoxLayout()
            question_layout.setSpacing(10)

            question_content = QLabel(f"Question: {question['content']}")
            question_content.setStyleSheet("font-weight: bold; font-size: 16px;")
            question_layout.addWidget(question_content)

            if question['image']:
                image_label = QLabel()
                image_url = question['image']['file']
                image_data = requests.get(image_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                image_label.setPixmap(pixmap.scaledToWidth(400, Qt.SmoothTransformation))
                image_label.setAlignment(Qt.AlignCenter)
                image_label.setStyleSheet("margin: 10px 0;")
                question_layout.addWidget(image_label)

            answer_count = 1
            for answer in question['answers']:
                answer_content = QLabel(f"Answer {answer_count}: {answer['content']}")
                answer_content.setStyleSheet("margin-left: 20px;")
                question_layout.addWidget(answer_content)
                answer_count += 1

            arr_list_answer = [item for item in question['answers'] if item['isResult'] == True]

            if len(arr_list_answer) > 0:
                right_label_content = QLabel("Right answer:")
                right_label_content.setStyleSheet("font-weight: bold; margin-top: 10px;")
                question_layout.addWidget(right_label_content)
                for answer in arr_list_answer:
                    right_content = QLabel(f"- {answer['content']}")
                    right_content.setStyleSheet("margin-left: 20px;")
                    question_layout.addWidget(right_content)

            question_box.setLayout(question_layout)
            scroll_layout.addWidget(question_box)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        self.setLayout(layout)
        self.setMinimumSize(1000, 500)

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

        duration_label = QLabel(f"Duration: {exam['duration']}")
        duration_label.setStyleSheet("""
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
        card_layout.addWidget(duration_label)
        card_layout.addWidget(total_question_label)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignLeft)

        detail_button = QPushButton("Detail")
        detail_button.setFixedWidth(100)
        detail_button.setStyleSheet("""
            QPushButton {
                background-color: #04AA6D;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005234;
            }
            QPushButton:pressed {
                background-color: #005234;
            }
        """)
        detail_button.clicked.connect(lambda: self.detail(exam['questions']))

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

        button_layout.addWidget(detail_button)
        button_layout.addWidget(delete_button)

        card_layout.addLayout(button_layout)

        card.setLayout(card_layout)
        
        self.cards_layout.addWidget(card)


    def delete(self, exam_id):
        dialog = DeleteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.exam_service.delete_exam(exam_id)
            self.get()

    def detail(self, questions):
        dialog = Detail(self, questions)
        if dialog.exec_() == QDialog.Accepted:
            self.get()

    