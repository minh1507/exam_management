from PyQt5.QtWidgets import QAction, QStackedWidget
from ..view import Home, Subject, Permission, Account


def body(self):
    self.stacked_widget = QStackedWidget()

    self.home = Home()
    self.subject = Subject()
    self.permission = Permission()
    self.account = Account()

    self.stacked_widget.addWidget(self.home)
    self.stacked_widget.addWidget(self.subject)
    self.stacked_widget.addWidget(self.permission)
    self.stacked_widget.addWidget(self.account)

    home = QAction('Home', self)
    subject = QAction('Subject', self)
    permission = QAction('Permission', self)
    account = QAction('Account', self)

    home.triggered.connect(self.showHome)
    subject.triggered.connect(self.showSubject)
    permission.triggered.connect(self.showPermission)
    account.triggered.connect(self.showAccount)

    body = dict()

    # action
    body["action"] = dict()
    body["action"]["home"] = home
    body["action"]["subject"] = subject
    body["action"]["permission"] = permission
    body["action"]["account"] = account

    body["main"] = self.stacked_widget
    return body
