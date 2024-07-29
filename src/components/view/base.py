from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from ..layout.breadcrumb import Breadcrumb

class ScrollableWidget(QWidget):
    breadcrumbs = []
    def __init__(self, parent=None):
        super().__init__(parent)
        

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignTop)

        if len(self.breadcrumbs):
            breadcrumb = Breadcrumb()
            for item in self.breadcrumbs:
                breadcrumb.add_crumb(item)
            self.content_layout.addWidget(breadcrumb)
        
        self.content_widget.setLayout(self.content_layout)
        scroll_area.setWidget(self.content_widget)
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)
