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

    home_action = QAction('Home', self)
    subject_action = QAction('Subject', self)
    permission_action = QAction('Permission', self)
    account_action = QAction('Account', self)

    # Connect actions to slots
    home_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.home))
    subject_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.subject))
    permission_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.permission))
    account_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.account))

    body = dict()

    body["action"] = dict()
    body["action"]["home"] = home_action
    body["action"]["subject"] = subject_action
    body["action"]["permission"] = permission_action
    body["action"]["account"] = account_action

    body["main"] = self.stacked_widget
    return body
