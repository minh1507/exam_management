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
    
    home_button = QToolButton()
    home_button.setDefaultAction(action["home"])
    home_button.setText(self.app.trans.objectT("home"))
    home_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    category_menu = QMenu("Category")
    category_menu.addAction(action["subject"])
    category_button = QToolButton()
    category_button.setText(self.app.trans.objectT("category"))
    category_button.setMenu(category_menu)
    category_button.setPopupMode(QToolButton.InstantPopup)
    category_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    corrector_menu = QMenu("corrector")
    corrector_menu.addAction(action["question"])
    corrector_button = QToolButton()
    corrector_button.setText(self.app.trans.objectT("corrector"))
    corrector_button.setMenu(corrector_menu)
    corrector_button.setPopupMode(QToolButton.InstantPopup)
    corrector_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    presenter_menu = QMenu("presenter")
    presenter_menu.addAction(action["exam"])
    presenter_button = QToolButton()
    presenter_button.setText(self.app.trans.objectT("presenter"))
    presenter_button.setMenu(presenter_menu)
    presenter_button.setPopupMode(QToolButton.InstantPopup)
    presenter_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    system_menu = QMenu("System")
    system_menu.addAction(action["role"])
    system_menu.addAction(action["account"])
    system_button = QToolButton()
    system_button.setText(self.app.trans.objectT("system"))
    system_button.setMenu(system_menu)
    system_button.setPopupMode(QToolButton.InstantPopup)
    system_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    preference_menu = QMenu("Setting")
    preference_menu.addAction(action["preference"])
    preference_button = QToolButton()
    preference_button.setText(self.app.trans.objectT("setting"))
    preference_button.setMenu(preference_menu)
    preference_button.setPopupMode(QToolButton.InstantPopup)
    preference_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    logout_action = QAction("Logout", self)
    logout_action.triggered.connect(lambda: logout(self, login_window))
    logout_button = QToolButton()
    logout_button.setDefaultAction(logout_action)
    logout_button.setText(self.app.trans.objectT("logout"))
    logout_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)

    role_code = Global.data["data"]["role"]["code"]
    if role_code == "ADMIN":
        toolbar_widget.addWidget(home_button)
        toolbar_widget.addWidget(category_button)
        toolbar_widget.addWidget(presenter_button)
        toolbar_widget.addWidget(corrector_button)
        toolbar_widget.addWidget(system_button)
        toolbar_widget.addWidget(preference_button)
        toolbar_widget.addWidget(logout_button)
    elif role_code == "EXAM_CORECTOR":
        toolbar_widget.addWidget(corrector_button)
        toolbar_widget.addWidget(preference_button)
        toolbar_widget.addWidget(logout_button)
    elif role_code == "EXAM_PRESENTER":
        toolbar_widget.addWidget(presenter_button)
        toolbar_widget.addWidget(preference_button)
        toolbar_widget.addWidget(logout_button)
    return toolbar_widget


