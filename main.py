from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *

from pyqtgameboards.gameboard import QHexagonboard
from gui.main_window import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    # overlays = []
    #
    # overlay1brush = QBrush(QColor(0, 255, 0, 150))
    # overlay1pen = QPen(QColor(0, 255, 0), 3, Qt.DashDotLine)
    #
    # overlay1dict = {
    #     "Brush": overlay1brush,
    #     "Pen": overlay1pen,
    #     "Positions": [
    #         [1, 1],
    #         [2, 1],
    #         [1, 2],
    #         [3, 3],
    #     ],
    # }
    #
    # overlays.append(overlay1dict)
    #
    # global app
    # app = QApplication(sys.argv)
    # global main
    # main = QMainWindow()
    #
    # main.setCentralWidget(QHexagonboard(
    #     horizontal=True,
    #     rows=20,
    #     columns=10,
    #     overlays=overlays,
    # ))
    #
    #
    # main.showMaximized()
    # sys.exit(app.exec_())

