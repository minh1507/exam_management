from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QTableWidgetItem, QTableWidget, QFrame
from PyQt5.QtCore import Qt
from ..layout.breadcrumb import Breadcrumb

class Subject(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignTop)

        breadcrumb = Breadcrumb()
        breadcrumb.add_crumb("Home", callback=lambda: print("Home clicked"))
        breadcrumb.add_crumb("Category", callback=lambda: print("Category clicked"))
        content_layout.addWidget(breadcrumb)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        content_layout.addWidget(line)

        table_widget = QTableWidget()
        table_widget.setRowCount(4) 
        table_widget.setColumnCount(3) 
        
        table_widget.setHorizontalHeaderLabels(['Order', 'Code', 'Name'])
        
        data = [
            ['Row 1, Col 1', 'Row 1, Col 2', 'Row 1, Col 3'],
            ['Row 2, Col 1', 'Row 2, Col 2', 'Row 2, Col 3'],
            ['Row 3, Col 1', 'Row 3, Col 2', 'Row 3, Col 3'],
            ['Row 4, Col 1', 'Row 4, Col 2', 'Row 4, Col 3'],
        ]
        
        for row in range(4):
            for col in range(3):
                table_widget.setItem(row, col, QTableWidgetItem(data[row][col]))
        
        content_layout.addWidget(table_widget)

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)

        layout.addWidget(scroll_area)
        self.setLayout(layout)
