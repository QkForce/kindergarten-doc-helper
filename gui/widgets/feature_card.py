from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QFrame,
    QGraphicsDropShadowEffect,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


class FeatureCard(QFrame):
    clicked = Signal()

    def __init__(self, title, description, icon_text):
        super().__init__()
        self.setFixedSize(280, 340)
        self.setObjectName("feature_card")
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Icon
        self.icon_label = QLabel(icon_text)
        self.icon_label.setObjectName("card_icon")

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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
