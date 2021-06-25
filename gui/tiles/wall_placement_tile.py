from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt


class WallPlacementTile(QWidget):
    def __init__(self, color, row, col):
        super(WallPlacementTile, self).__init__()
        self.setStyleSheet("background: " + color + ";")

        self.row = row
        self.col = col
        self.setFixedSize(50, 50)

    # def mousePressEvent(self, event):
    #     self.main_window.click_on_tile(self.row, self.col)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def set_cursor_pointing(self, clickable):
        if clickable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setStyleSheet("background: #c95e06")
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
