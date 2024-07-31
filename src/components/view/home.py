from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from .base import ScrollableWidget

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

class Home(ScrollableWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        card1 = self.create_summary_card("Total Users", "1500")
        card2 = self.create_summary_card("Active Sessions", "300")
        card3 = self.create_summary_card("New Signups", "50")

        top_layout.addWidget(card1)
        top_layout.addWidget(card2)
        top_layout.addWidget(card3)

        main_layout.addLayout(top_layout)

        middle_layout = QVBoxLayout()

        sc1 = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot_bar_chart(sc1.axes)

        sc2 = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot_line_chart(sc2.axes)

        sc3 = MplCanvas(self, width=5, height=4, dpi=100)
        self.plot_pie_chart(sc3.axes)

        chart_layout = QHBoxLayout()
        chart_layout.addWidget(sc1)
        chart_layout.addWidget(sc2)
        chart_layout.addWidget(sc3)

        middle_layout.addLayout(chart_layout)
        main_layout.addLayout(middle_layout)

        bottom_layout = QHBoxLayout()

        example_button = QPushButton("View Details")
        example_button.setStyleSheet("padding: 10px; font-size: 14px;")
        bottom_layout.addWidget(example_button)

        main_layout.addLayout(bottom_layout)

        self.content_layout.addLayout(main_layout)

    def create_summary_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("border: 1px solid #ccc; border-radius: 10px; padding: 10px; background-color: #f9f9f9;")
        card_layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #007bff;")
        value_label.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        card.setLayout(card_layout)

        return card

    def plot_bar_chart(self, axes):
        labels = ['A', 'B', 'C', 'D', 'E']
        values = [10, 20, 15, 25, 30]

        axes.bar(labels, values)
        axes.set_title('Example Bar Chart')
        axes.set_xlabel('Categories')
        axes.set_ylabel('Values')

    def plot_line_chart(self, axes):
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 7, 11]

        axes.plot(x, y, marker='o')
        axes.set_title('Example Line Chart')
        axes.set_xlabel('X Axis')
        axes.set_ylabel('Y Axis')

    def plot_pie_chart(self, axes):
        labels = ['A', 'B', 'C', 'D']
        sizes = [15, 30, 45, 10]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

        axes.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        axes.set_title('Example Pie Chart')

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = Home()
    window.show()
    sys.exit(app.exec_())
