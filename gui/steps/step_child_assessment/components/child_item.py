from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)

from gui.utils.icon_utils import get_svg_pixmap
from gui.constants.icons import IconPaths
from gui.constants.colors import AppColors
from logic.types import AssessmentStatus


class ChildItemWidget(QWidget):
    def __init__(self, name, status=AssessmentStatus.NOT_STARTED, parent=None):
        super().__init__(parent)
        self.setObjectName("child_item")

        # Child's name
        self.name_label = QLabel(name)
        # Status marker (circle)
        self.status_icon = QLabel()
        self.setStatus(status)

        layout = QHBoxLayout(self)
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.status_icon)

    def setSelected(self, selected):
        self.name_label.setProperty("selected", selected)
        self.style().unpolish(self.name_label)
        self.style().polish(self.name_label)

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
