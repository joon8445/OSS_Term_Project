import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import chart
from data_manager import read_predict

form_class = uic.loadUiType("user.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.comboBox.activated[str].connect(self.clicked)

    def initUI(self):
        self.fig = plt.Figure()
        combo = self.comboBox.currentText()
        self.canvas = FigureCanvas(self.fig)
        self.chart.addWidget(self.canvas)
        chart.draw_chart(self, combo)
        self.canvas.draw()
        self.prediction.append(read_predict(combo))
    def clicked(self, text):
        self.clear()
        self.prediction.append(read_predict(text))
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.chart.addWidget(self.canvas)
        chart.draw_chart(self, text)
        self.canvas.draw()

    def clear(self):
        self.prediction.clear()

        tmp = self.chart
        if tmp is not None:
            while tmp.count():
                item = tmp.takeAt(0)

                widget = item.widget()

                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearvbox(item.layout())

if __name__== "__main__" :
    app = QApplication(sys.argv)

    myWindow = WindowClass()

    myWindow.show()

    app.exec_()