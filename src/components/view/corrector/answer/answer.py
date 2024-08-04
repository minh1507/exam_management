from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QDialog,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
    QSplitter,
    QWidget,
    QComboBox,
    QCheckBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../../"))
sys.path.append(project_root)
from src.services.answer import AnswerService

class CreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Create Question')
        self.setWindowIcon(QIcon("src/assets/icon/create.png"))
        self.parent = parent
        self.answerService = AnswerService()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        splitter = QSplitter(Qt.Vertical, self)
        splitter.setHandleWidth(10)

        form_widget = QWidget(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_widget.setLayout(form_layout)

        self.content_input = QLineEdit(self)
        self.content_input.setPlaceholderText("content")
        self.content_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Content'), self.content_input)

        self.result_checkbox = QCheckBox("Result", self)
        form_layout.addRow(self.result_checkbox)

        splitter.addWidget(form_widget)

        form_widget.setMinimumHeight(100)  

        layout.addWidget(splitter)

        submit_button = QPushButton("submit", self)
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

        cancel_button = QPushButton("cancel", self)
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

        layout.addLayout(button_layout)
        layout.setContentsMargins(20, 20, 20, 20) 

        self.setMinimumSize(500, 200)

    def set_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def get_data(self):
        return {
            'isResult': self.result_checkbox.isChecked(),
            'content': self.content_input.text(),
        }

class DeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Delete question')
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
    def __init__(self, answer, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Update Answer')
        self.setWindowIcon(QIcon("src/assets/icon/update.png"))
        self.answer = answer
        self.subjectService = AnswerService()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.content_input = QLineEdit(self)
        self.content_input.setPlaceholderText("content")
        self.content_input.setText(self.answer['content'])
        self.content_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Content'), self.content_input)

        self.result_checkbox = QCheckBox("Result", self)
        self.result_checkbox.setChecked(self.answer['isResult'])
        form_layout.addRow(self.result_checkbox)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-size: 12px;")
        self.error_label.setWordWrap(True)
        self.error_label.setVisible(False)
        form_layout.addRow(self.error_label)

        layout.addLayout(form_layout)

        submit_button = QPushButton("submit", self)
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

        cancel_button = QPushButton("cancel", self)
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

        layout.addLayout(button_layout)
        layout.setContentsMargins(20, 20, 20, 20)

        self.setMinimumSize(500, 200)

    def set_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def get_data(self):
        return {
            'isResult': self.result_checkbox.isChecked(),
            'content': self.content_input.text(),
        }

class Answer(QDialog):
    def __init__(self, question_id):
        super().__init__()
        self.setWindowTitle('Answer')
        self.answer_service = AnswerService()
        self.question_id = question_id
        self.init_ui()

    def init_ui(self):
        content_layout = QVBoxLayout(self)
        content_layout.setSpacing(10)

        # Add horizontal line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        content_layout.addWidget(line, alignment=Qt.AlignTop)

        # Add create button
        create_button = QPushButton("Create")
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
        content_layout.addWidget(create_button, alignment=Qt.AlignTop)

        # Add cards layout
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(10)
        content_layout.addLayout(self.cards_layout)

        content_layout.addStretch()
        self.setLayout(content_layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.get()
    
    def get(self):
        data = self.answer_service.fetch_answers(self.question_id)
        self.data = data
        self.clear_cards()

        for answer in self.data:
            self.create_card(answer)

    def clear_cards(self):
        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def create_card(self, answer):
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

        content_label = QLabel(f"{answer['content']}")
        content_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        """)

        card_layout.addWidget(content_label)

        check = "Yes"
        if answer['isResult'] == False:
            check = "No"


        result_label = QLabel(f"Result: {check}")
        result_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333;
        """)

        card_layout.addWidget(result_label)

        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 5, 5, 5)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignLeft)

        update_button = QPushButton("Update")
        update_button.setFixedWidth(100)
        update_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
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
        update_button.clicked.connect(lambda: self.update(answer))

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
        delete_button.clicked.connect(lambda: self.delete(answer['id']))

        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)

        card_layout.addLayout(button_layout)

        card.setLayout(card_layout)
        
        self.cards_layout.addWidget(card)

    def open_create_dialog(self):
        dialog = CreateDialog(self)
        while True:
            if dialog.exec_() == QDialog.Accepted:
                new_data = dialog.get_data()
                response = self.answer_service.create_answer(new_data, self.question_id)
                if response['status'] == 400:
                    dialog.set_error(self.trans.message(response["messages"][0]))
                    continue
                else:
                    self.get()
                    break
            else:
                break
    def delete(self, question_id):
        dialog = DeleteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.answer_service.delete_answer(question_id)
            self.get()
    def update(self, question):
        dialog = UpdateDialog(question, self)
        while True:
            if dialog.exec_() == QDialog.Accepted:
                updated_data = dialog.get_data()
                response = self.answer_service.update_answer(question['id'], updated_data, self.question_id)
                if response['status'] == 400:
                    dialog.set_error(self.trans.message(response["messages"][0]))
                    continue
                else:
                    self.get()
                    break
            else:
                break