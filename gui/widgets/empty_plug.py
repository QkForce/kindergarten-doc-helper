from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from gui.utils.icon_utils import get_svg_pixmap
from gui.constants.icons import IconPaths
from gui.constants.colors import AppColors


class EmptyPlug(QWidget):
    def __init__(self, title, description):
        super().__init__()

        icon_lbl = QLabel()
        icon_pixmap = get_svg_pixmap(
            icon_path=IconPaths.EMPTY, color=AppColors.CANVAS, size=48
        )
        icon_lbl.setPixmap(icon_pixmap)

        icon_layout = QVBoxLayout()
        icon_layout.addWidget(icon_lbl, alignment=Qt.AlignCenter)
        icon_frame = QFrame()
        icon_frame.setFixedSize(100, 100)
        icon_frame.setProperty("frame-style", "status-empty")
        icon_frame.setLayout(icon_layout)

        title_lbl = QLabel(title)
        title_lbl.setProperty("lbl-level", "h2")
        # title_lbl.setWordWrap(True)

        description_lbl = QLabel(description)
        description_lbl.setProperty("lbl-level", "h3-normal")
        # description_lbl.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(icon_frame, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(title_lbl, alignment=Qt.AlignCenter)
        layout.addWidget(description_lbl, alignment=Qt.AlignCenter)
        layout.addStretch()
