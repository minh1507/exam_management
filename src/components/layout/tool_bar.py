from PyQt5.QtWidgets import QToolBar, QAction, QStackedWidget

def tool_bar(self, action):
    toolbar_widget = QToolBar()
    toolbar_widget.setStyleSheet("""
            QToolBar {
                background-color: white;
                border: 1px solid grey;
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
    # toolbar_widget.addAction(action["action2"])

    return toolbar_widget

    