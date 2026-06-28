from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtGui import QIcon

from gui.constants.colors import AppColors
from gui.utils.icon_utils import get_svg_pixmap


class BadgeButton(QPushButton):
    def __init__(self, icon_path, label: str, text: str, parent=None):
        super().__init__(text, parent)
        self.setObjectName(f"badge_button")
        self.setProperty("btn-mid", "medium")
        self.setProperty("btn-type", "ghost")
        self.setFlat(True)
        self.label = label
        icon_pixmap = get_svg_pixmap(icon_path, AppColors.PRIMARY, 16)
        self.setIcon(QIcon(icon_pixmap))
        self.setText(text)

    def setText(self, text):
        text = f"{self.label}{text}" if self.label else text
        super().setText(text)


class ContextBadgeGroup(QWidget):
    def __init__(self, badges: list[BadgeButton], parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

        for badge in badges:
            self.layout.addWidget(badge)
