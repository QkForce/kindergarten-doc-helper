from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QFrame,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

from gui.constants.icons import IconPaths


class FeatureCard(QFrame):
    clicked = Signal()

    def __init__(self, title, description, icon_path: IconPaths):
        super().__init__()
        self.setFixedSize(280, 340)
        self.setObjectName("feature_card")
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setObjectName("card_icon")
        self.set_icon(icon_path)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("card_title")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignCenter)

        self.desc_label = QLabel(description)
        self.desc_label.setObjectName("card_desc")
        self.desc_label.setWordWrap(True)
        self.desc_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.icon_label, 0, Qt.AlignCenter)
        layout.addWidget(self.title_label)
        layout.addWidget(self.desc_label)
        layout.addStretch()

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)

    def set_icon(self, icon_path: str, size: int = 48):
        # 1. Create a blank transparent Pixmap
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        # 2. Create a Renderer to render the SVG
        renderer = QSvgRenderer(icon_path)

        if renderer.isValid():
            # 3. Using Painter to draw SVG on top of Pixmap
            painter = QPainter(pixmap)
            # Turn on anti-aliasing for smoother edges
            painter.setRenderHint(QPainter.Antialiasing)
            renderer.render(painter)
            painter.end()
            self.icon_label.setPixmap(pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
