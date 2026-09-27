from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)

from gui.utils.icon_utils import get_svg_pixmap
from gui.constants.icons import IconPaths
from gui.constants.colors import AppColors
from logic.types import AssessmentStatus


class SelectorItem(QWidget):
    def __init__(self, name, status=AssessmentStatus.NOT_STARTED, parent=None):
        super().__init__(parent)
        self.setObjectName("selector_item")

        # label for the item
        self.label = QLabel(name)
        # Status marker (circle)
        self.status_icon = QLabel()
        self.setStatus(status)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.status_icon)

    def setSelected(self, selected):
        self.label.setProperty("selected", selected)
        self.style().unpolish(self.label)
        self.style().polish(self.label)

    def setStatus(self, status: AssessmentStatus):
        if (
            not isinstance(status, AssessmentStatus)
            or status is AssessmentStatus.NOT_STARTED
        ):
            self.status_icon.clear()
            return
        icons = {
            AssessmentStatus.COMPLETED: (IconPaths.ENTRY_COMPLETED, AppColors.SUCCESS),
            AssessmentStatus.IN_PROGRESS: (IconPaths.ENTRY_PARTIAL, AppColors.WARNING),
        }
        icon_path, color = icons.get(status)
        pixmap = get_svg_pixmap(icon_path, color, size=14)
        self.status_icon.setPixmap(pixmap)
