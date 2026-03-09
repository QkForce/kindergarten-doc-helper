from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor


def apply_shadow(
    widget,
    color: QColor = QColor(0, 0, 0, 20),
    blur_radius: int = 25,
    offset_x: int = 0,
    offset_y: int = 8,
):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur_radius)
    shadow.setXOffset(offset_x)
    shadow.setYOffset(offset_y)
    shadow.setColor(color)
    widget.setGraphicsEffect(shadow)
