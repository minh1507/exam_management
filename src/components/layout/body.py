from PyQt5.QtWidgets import QAction, QStackedWidget
from ..view import Home, View2

def body(self):
    self.stacked_widget = QStackedWidget()

    self.home = Home()
    self.view2 = View2()
    self.stacked_widget.addWidget(self.home)
    self.stacked_widget.addWidget(self.view2)

    home = QAction('Home', self)
    action2 = QAction('Action 2', self)

    home.triggered.connect(self.showHome)
    action2.triggered.connect(self.showView2)

    body = dict()

    #action
    body["action"] = dict()
    body["action"]["home"] = home
    body["action"]["action2"] = action2

    body["main"] = self.stacked_widget
    return body

    