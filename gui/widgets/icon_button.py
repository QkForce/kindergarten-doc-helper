from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QSize, Property
from PySide6.QtGui import QColor, QIcon

from gui.constants.colors import AppColors
from gui.utils.icon_utils import get_svg_pixmap


class IconButton(QPushButton):
    def __init__(
        self,
        icon_path="",
        icon_size=16,
        text="",
        current_color=AppColors.BTN_GHOST_TEXT,
        hover_color=AppColors.BTN_GHOST_HOVER_TEXT,
        parent=None,
    ):
        super().__init__(text, parent)
        self._icon_path = icon_path
        self._icon_size = icon_size
        self._current_color = current_color
        self._hover_color = hover_color
        self._is_hovered = False
        self.setIcon(
            QIcon(get_svg_pixmap(self._icon_path, self._current_color, self._icon_size))
        )

    def setIconPath(self, icon_path):
        self._icon_path = icon_path
        self._update_icon(self._current_color)

    @Property(QColor)
    def iconColor(self):
        return QColor(self._current_color)

    @iconColor.setter
    def iconColor(self, color):
        self._current_color = color.name()
        if not self._is_hovered:
            self._update_icon(self._current_color)

    @Property(QColor)
    def hoverColor(self):
        return QColor(self._hover_color)

    @hoverColor.setter
    def hoverColor(self, color):
        self._hover_color = self._hover_color or color.name()

    def _update_icon(self, color_hex):
        if self._icon_path:
            pixmap = get_svg_pixmap(self._icon_path, color_hex, self._icon_size)
            self.setIcon(QIcon(pixmap))
            self.setIconSize(QSize(self._icon_size, self._icon_size))

    def enterEvent(self, event):
        super().enterEvent(event)
        self._is_hovered = True
        self._update_icon(self._hover_color)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self._is_hovered = False
        self._update_icon(self._current_color)
