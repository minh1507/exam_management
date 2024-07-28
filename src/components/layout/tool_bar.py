from PyQt5.QtWidgets import QToolBar, QMenu, QToolButton
from PyQt5.QtCore import Qt

def tool_bar(self, action):
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

    toolbar_widget.addAction(action["home"])

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
    toolbar_widget.addWidget(category_button)

    system_menu = QMenu("System")
    system_menu.addAction(action["permission"])
    system_button = QToolButton()
    system_button.setText("System")
    system_button.setMenu(system_menu)
    system_button.setPopupMode(QToolButton.InstantPopup)  
    system_button.setStyleSheet("""
        QToolButton::menu-indicator {
            image: none;
        }
    """)
    toolbar_widget.addWidget(system_button)
    
    return toolbar_widget

    