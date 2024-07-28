from PyQt5.QtWidgets import QAction, QStackedWidget
from ..view import Home, Subject

def body(self):
    self.stacked_widget = QStackedWidget()

    self.home = Home()
    self.subject = Subject()
    self.stacked_widget.addWidget(self.home)
    self.stacked_widget.addWidget(self.subject)

    home = QAction('Home', self)
    subject = QAction('Subject', self)

    home.triggered.connect(self.showHome)
    subject.triggered.connect(self.showSubject)

    body = dict()

    #action
    body["action"] = dict()
    body["action"]["home"] = home
    body["action"]["subject"] = subject

    body["main"] = self.stacked_widget
    return body

    