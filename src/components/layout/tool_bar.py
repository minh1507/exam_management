from PyQt5.QtWidgets import QToolBar, QMenu, QToolButton, QAction
import sys
import os

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../"))
sys.path.append(project_root)
from src.common.static.global_c import Global

def logout(self, login_window):
        Global.token = None
        Global.data = None
        self.close()
        login_window.show()

def tool_bar(self, action, login_window):
    toolbar_widget = QToolBar()

    toolbar_widget.setStyleSheet("""
            QToolBar {
                background-color: white;
                border: 1px solid grey;
                padding: unset !important;
            }
            QToolBar QToolButton {
                color: black;
            }
            QToolBar QToolButton:hover {
                color: black;
                border: unset !important;
                background-color: #cccccc !important;
            }
        """)

    category_menu = QMenu("Category")
    category_menu.addAction(action["subject"])
    category_button = QToolButton()
    category_button.setText("Category")
    category_button.setMenu(category_menu)
    category_button.setPopupMode(QToolButton.InstantPopup)
    category_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    system_menu = QMenu("System")
    system_menu.addAction(action["role"])
    system_menu.addAction(action["account"])
    system_button = QToolButton()
    system_button.setText("System")
    system_button.setMenu(system_menu)
    system_button.setPopupMode(QToolButton.InstantPopup)
    system_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    logout_action = QAction("Logout", self)
    logout_action.triggered.connect(lambda: logout(self, login_window))
    logout_button = QToolButton()
    logout_button.setText("Logout")
    logout_button.setDefaultAction(logout_action)
    logout_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    #permission
    role_code = Global.data["data"]["role"]["code"]
    if role_code == "ADMIN":
        toolbar_widget.addAction(action["home"])
        toolbar_widget.addWidget(category_button)
        toolbar_widget.addWidget(system_button)
        toolbar_widget.addWidget(logout_button)
    if role_code == "EXAM_ENTRANTS":
        toolbar_widget.addWidget(logout_button)

    return toolbar_widget


