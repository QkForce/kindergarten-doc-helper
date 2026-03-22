from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QTransform


class RotatingIcon(QLabel):
    def __init__(self, pixmap, initial_angle=0, parent=None):
        super().__init__(parent)
        self.src_pixmap = pixmap
        self.angle = initial_angle
        self.setPixmap(self.src_pixmap)

    def rotate(self, angle):
        self.angle = angle
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Центрге қатысты бұру
        transform = QTransform()
        transform.translate(self.width() / 2, self.height() / 2)
        transform.rotate(self.angle)
        transform.translate(-self.width() / 2, -self.height() / 2)

        painter.setTransform(transform)
        painter.drawPixmap(self.rect(), self.src_pixmap)
        painter.end()
