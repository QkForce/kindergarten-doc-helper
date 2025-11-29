from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor


def apply_shadow(widget):
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(25)
    effect.setOffset(0, 4)
    effect.setColor(QColor(0, 0, 0, 60))  # жұмсақ қара
    widget.setGraphicsEffect(effect)
