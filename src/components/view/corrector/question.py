from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QDialog,
    QLineEdit,
    QFormLayout,
    QHBoxLayout,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QCoreApplication, QUrl
from PyQt5.QtCore import Qt
import sys
import os
from ..base import ScrollableWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QFileDialog, QCheckBox, QSizePolicy, QSplitter, QWidget, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../"))
sys.path.append(project_root)
from src.services.question import QuestionService
from src.common.i18n.lang import Trans
from src.services.subject import SubjectService
from src.common.helper.string import StringHelper

class CreateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Create Question')
        self.setWindowIcon(QIcon("src/assets/icon/create.png"))
        self.parent = parent
        self.subjectService = SubjectService()
        self.init_ui()

    def init_ui(self):
        self.subjects = self.subjectService.fetch_subjects()

        layout = QVBoxLayout(self)

        splitter = QSplitter(Qt.Vertical, self)
        splitter.setHandleWidth(10)

        form_widget = QWidget(self)
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_widget.setLayout(form_layout)

        self.lecturer_input = QLineEdit(self)
        self.lecturer_input.setPlaceholderText("lecturer")
        self.lecturer_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Lecturer'), self.lecturer_input)

        self.content_input = QLineEdit(self)
        self.content_input.setPlaceholderText("content")
        self.content_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Content'), self.content_input)

        self.mark_input = QLineEdit(self)
        self.mark_input.setPlaceholderText("mark")
        self.mark_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Mark'), self.mark_input)

        self.unit_input = QLineEdit(self)
        self.unit_input.setPlaceholderText("unit")
        self.unit_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Unit'), self.unit_input)

        self.subject_input = QComboBox(self)
        self.subject_input.addItems([subject['name'] for subject in self.subjects])
        self.subject_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Subject'), self.subject_input)

        self.mix_choices_checkbox = QCheckBox("mixChoices", self)
        form_layout.addRow(self.mix_choices_checkbox)

        image_widget = QWidget(self)
        image_layout = QVBoxLayout()
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setPixmap(QPixmap()) 
        self.image_label.setScaledContents(False)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setMaximumHeight(300)  
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.open_file_dialog)

        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.upload_button)
        image_layout.setAlignment(Qt.AlignCenter)
        image_widget.setLayout(image_layout)

        splitter.addWidget(form_widget)
        splitter.addWidget(image_widget)

        form_widget.setMinimumHeight(300)  
        image_widget.setMinimumHeight(200) 

        layout.addWidget(splitter)

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

        layout.addLayout(button_layout)
        layout.setContentsMargins(20, 20, 20, 20) 

        self.setMinimumSize(500, 400)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
        if file_name:
            self.display_image(file_name)

    def display_image(self, file_name):
        pixmap = QPixmap(file_name)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap)
            self.adjust_label_size(pixmap)

    def adjust_label_size(self, pixmap):
        max_width = self.width() - 40  
        width = min(max_width, pixmap.width())
        height = int(width * 9 / 16)
        
        scaled_pixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

    def set_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def get_data(self):
        return {
            'lecturer': self.lecturer_input.text(),
            'content': self.content_input.text(),
            'mark': self.mark_input.text(),
            'unit': self.unit_input.text(),
            'subject': next((subject['id'] for subject in self.subjects if subject['name'] == self.subject_input.currentText()), None),
            'mixChoices': self.mix_choices_checkbox.isChecked(),
            'image': self.image_label.pixmap() 
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
    def __init__(self, question, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Update Question')
        self.setWindowIcon(QIcon("src/assets/icon/update.png"))
        self.question = question
        self.subjectService = SubjectService()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.sub = self.subjectService.fetch_subjects()
        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.lecturer_input = QLineEdit(self)
        self.lecturer_input.setText(self.question['lecturer'])
        self.lecturer_input.setPlaceholderText("lecturer")
        self.lecturer_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Lecturer'), self.lecturer_input)

        self.content_input = QLineEdit(self)
        self.content_input.setText(self.question['content'])
        self.content_input.setPlaceholderText("content")
        self.content_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Content'), self.content_input)

        self.mark_input = QLineEdit(self)
        self.mark_input.setText(str(self.question['mark']))
        self.mark_input.setPlaceholderText("mark")
        self.mark_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Mark'), self.mark_input)

        self.unit_input = QLineEdit(self)
        self.unit_input.setText(self.question['unit'])
        self.unit_input.setPlaceholderText("unit")
        self.unit_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Unit'), self.unit_input)

        self.subject_input = QComboBox(self)
        self.subject_input.addItems([subject['name'] for subject in self.sub])
        self.subject_input.setCurrentText(self.question['subject']['name'])
        self.subject_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 5px;")
        form_layout.addRow(QLabel('Subject'), self.subject_input)

        self.mix_choices_checkbox = QCheckBox("mixChoices", self)
        self.mix_choices_checkbox.setChecked(self.question['mixChoices'])
        form_layout.addRow(self.mix_choices_checkbox)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red; font-size: 12px;")
        self.error_label.setWordWrap(True)
        self.error_label.setVisible(False)
        form_layout.addRow(self.error_label)

        layout.addLayout(form_layout)

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

        layout.addLayout(button_layout)
        layout.setContentsMargins(20, 20, 20, 20)

        self.setMinimumSize(500, 500)

    def handle_image_response(self, reply):
        if reply.error() == QNetworkReply.NoError:
            image_data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.image_label.setPixmap(pixmap.scaled(400, 225, Qt.KeepAspectRatio))
        else:
            self.set_error("Failed to load image.")
            print(f"Error loading image: {reply.errorString()}")  

    def set_error(self, message):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def get_data(self):
        return {
            'lecturer': self.lecturer_input.text(),
            'content': self.content_input.text(),
            'mark': self.mark_input.text(),
            'unit': self.unit_input.text(),
            'subject': next((subject['id'] for subject in self.sub if subject['name'] == self.subject_input.currentText()), None),
            'mixChoices': self.mix_choices_checkbox.isChecked(),
        }


class Question(ScrollableWidget):
    breadcrumbs = ["Home", "Corrector", "Question"]

    def __init__(self):
        super().__init__()
        self.question_service = QuestionService()
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
                response = self.question_service.create_question(new_data)
                if response['status'] == 400:
                    dialog.set_error(self.trans.message(response["messages"][0]))
                    continue
                else:
                    self.get()
                    break
            else:
                break

    def get(self):
        data = self.question_service.fetch_questions()
        self.data = data
        self.clear_cards()

        for question in self.data:
            self.create_card(question)

    def clear_cards(self):
        for i in reversed(range(self.cards_layout.count())):
            widget = self.cards_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def create_card(self, question):
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

        content_label = QLabel(f"{question['content']}")
        content_label.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        """)

        card_width = card.width() - 20
        pixmap = self.load_image(question['image']['file'])
        image_height = int(card_width * pixmap.height() / pixmap.width())
        scaled_pixmap = pixmap.scaled(card_width, image_height, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        lecturer_label = QLabel(f"Lecturer: {question['lecturer']}")
        lecturer_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)

        mark_label = QLabel(f"Mark: {StringHelper.parse_question_mark(question['mark'])}")
        mark_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)

        subject_label = QLabel(f"Subject: {question['subject']['name']}")
        subject_label.setStyleSheet("""
            font-size: 14px;
            color: #555;
        """)
       
        card_layout.addWidget(content_label)
        card_layout.addWidget(image_label)
        card_layout.addWidget(subject_label)
        card_layout.addWidget(lecturer_label)
        card_layout.addWidget(mark_label)

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
        update_button.clicked.connect(lambda: self.update(question))

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
        delete_button.clicked.connect(lambda: self.delete(question['id']))

        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)

        card_layout.addLayout(button_layout)

        card.setLayout(card_layout)
        
        self.cards_layout.addWidget(card)


    def delete(self, question_id):
        dialog = DeleteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.question_service.delete_question(question_id)
            self.get()

    def update(self, question):
        dialog = UpdateDialog(question, self)
        while True:
            if dialog.exec_() == QDialog.Accepted:
                updated_data = dialog.get_data()
                response = self.question_service.update_question(question['id'], updated_data, question["image"]['id'])
                if response['status'] == 400:
                    dialog.set_error(self.trans.message(response["messages"][0]))
                    continue
                else:
                    self.get()
                    break
            else:
                break
    def load_image(self, url):
        pixmap = QPixmap()
        pixmap.loadFromData(self.download_image(url))
        return pixmap

    def download_image(self, url):
        manager = QNetworkAccessManager()
        request = QNetworkRequest(QUrl(url))
        reply = manager.get(request)
        while not reply.isFinished():
            QCoreApplication.processEvents()
        return reply.readAll()


