from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QPushButton,
    QWidget
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
from src.common.i18n.lang import Trans

class Preference(QWidget):
    breadcrumbs = ["Home", "Preference"]

    def __init__(self):
        super().__init__()
        self.selected_option = "English"  
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)  

        title_label = QLabel("Choose Left or Right and Hit the Button")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 20px;
        """)
        main_layout.addWidget(title_label)

        self.action_button = QPushButton("English")  
        self.action_button.setStyleSheet("""
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-size: 16px;
            width: 200px;
        """)
        self.action_button.clicked.connect(self.toggle_option)
        main_layout.addWidget(self.action_button)

        self.setLayout(main_layout)

    def toggle_option(self):
        if self.selected_option == "English":
            self.selected_option = "Vietnamese"
            self.action_button.setText("Vietnamese")
            Trans.language = "vi"
        else:
            self.selected_option = "English"
            self.action_button.setText("English")
            Trans.language = "en"
        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = Preference()
    window.setGeometry(100, 100, 400, 200) 
    window.show()
    sys.exit(app.exec_())
