from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QColor, QPen


class Spinner(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)
        self.setContentsMargins(0, 0, 0, 0)

    def rotate(self):
        self.angle = (self.angle + 30) % 360
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.translate(self.width() / 2, self.height() / 2)
        p.rotate(self.angle)

        pen = QPen(QColor("#4f46e5"), 4)
        p.setPen(pen)
        p.drawArc(-12, -12, 24, 24, 0, 270 * 16)
