from PyQt5.QtWidgets import QAction, QStackedWidget
from ..view import Home, Subject, Role, Account, Preference, Question

def body(self):
    self.stacked_widget = QStackedWidget()

    self.home = Home()
    self.subject = Subject()
    self.role = Role()
    self.account = Account()
    self.preference = Preference()
    self.question = Question()

    self.stacked_widget.addWidget(self.home)
    self.stacked_widget.addWidget(self.subject)
    self.stacked_widget.addWidget(self.role)
    self.stacked_widget.addWidget(self.account)
    self.stacked_widget.addWidget(self.preference)
    self.stacked_widget.addWidget(self.question)

    home_action = QAction('Home', self)
    subject_action = QAction(self.app.trans.objectT("subject"), self)
    role_action = QAction(self.app.trans.objectT("role"), self)
    account_action = QAction(self.app.trans.objectT("account"), self)
    preference_action = QAction(self.app.trans.objectT("preference"), self)
    question_action = QAction(self.app.trans.objectT("question"), self)

    home_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.home))
    subject_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.subject))
    role_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.role))
    account_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.account))
    preference_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.preference))
    question_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.question))

    body = dict()

    body["action"] = dict()
    body["action"]["home"] = home_action
    body["action"]["subject"] = subject_action
    body["action"]["role"] = role_action
    body["action"]["account"] = account_action
    body["action"]["preference"] = preference_action
    body["action"]["question"] = question_action

    body["main"] = self.stacked_widget
    return body
