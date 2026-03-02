from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)

from gui.utils.icon_utils import get_svg_pixmap
from gui.constants.icons import IconPaths
from gui.constants.colors import AppColors


class ChildItemWidget(QWidget):
    def __init__(self, name, status="empty", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        # Status marker (circle)
        self.status_icon = QLabel()
        self.setStatus(status)

        # Child's name
        self.name_label = QLabel(name)

        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.status_icon)

    def setSelected(self, selected):
        self.name_label.setProperty("lbl-selected", selected)
        self.style().unpolish(self.name_label)
        self.style().polish(self.name_label)

    def setStatus(self, status):
        if status == "empty":
            self.status_icon.clear()
            return
        icons = {
            "success": (IconPaths.ENTRY_COMPLETED, AppColors.SUCCESS),
            "partial": (IconPaths.ENTRY_PARTIAL, AppColors.WARNING),
        }
        icon_path, color = icons.get(status, (None, None))
        pixmap = get_svg_pixmap(icon_path, color, size=14)
        self.status_icon.setPixmap(pixmap)
