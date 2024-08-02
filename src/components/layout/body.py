from PyQt5.QtWidgets import QAction, QStackedWidget
from ..view import Home, Subject, Role, Account, Preference

def body(self):
    self.stacked_widget = QStackedWidget()

    self.home = Home()
    self.subject = Subject()
    self.role = Role()
    self.account = Account()
    self.preference = Preference()

    self.stacked_widget.addWidget(self.home)
    self.stacked_widget.addWidget(self.subject)
    self.stacked_widget.addWidget(self.role)
    self.stacked_widget.addWidget(self.account)
    self.stacked_widget.addWidget(self.preference)

    home_action = QAction('Home', self)
    subject_action = QAction(self.app.trans.objectT("subject"), self)
    role_action = QAction(self.app.trans.objectT("role"), self)
    account_action = QAction(self.app.trans.objectT("account"), self)
    preference_action = QAction(self.app.trans.objectT("preference"), self)

    # Connect actions to slots
    home_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.home))
    subject_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.subject))
    role_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.role))
    account_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.account))
    preference_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.preference))

    body = dict()

    body["action"] = dict()
    body["action"]["home"] = home_action
    body["action"]["subject"] = subject_action
    body["action"]["role"] = role_action
    body["action"]["account"] = account_action
    body["action"]["preference"] = preference_action

    body["main"] = self.stacked_widget
    return body
