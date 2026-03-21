from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPainter, QColor, QPen

from gui.constants.colors import AppColors


class Spinner(QWidget):
    def __init__(self, color=AppColors.PRIMARY, size=24, speed=50):
        super().__init__()
        self.angle = 0
        self.spinner_color = QColor(color)
        self.spinner_size = size

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)

        self.hide()

    def rotate(self):
        self.angle = (self.angle + 30) % 360
        self.update()

    def start_animation(self):
        if not self.timer.isActive():
            self.show()
            self.timer.start(50)

    def stop_animation(self):
        self.timer.stop()
        self.hide()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Центрге жылжыту
        p.translate(self.width() / 2, self.height() / 2)
        p.rotate(self.angle)

        pen = QPen(self.spinner_color, 4)
        pen.setCapStyle(Qt.RoundCap)  # Ұштарын жұмсарту (әдемірек көрінеді)
        p.setPen(pen)

        # Өлшемді динамикалық түрде есептеу
        r = self.spinner_size / 2
        p.drawArc(-r, -r, self.spinner_size, self.spinner_size, 0, 270 * 16)
