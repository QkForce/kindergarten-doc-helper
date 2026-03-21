from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Qt

from gui.widgets.spinner import Spinner
from gui.constants.colors import AppColors


class LoadingPlug(QWidget):
    def __init__(self, title="title", description="description"):
        super().__init__()
        self.title = title
        self.description = description

        spinner = Spinner(color=AppColors.PRIMARY, size=48)
        spinner.start_animation()
        spinner.setFixedWidth(100)
        spinner.setFixedHeight(100)
        title = QLabel(title)
        title.setProperty("lbl-level", "h2")
        description = QLabel(description)
        description.setProperty("lbl-level", "h3-normal")

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(spinner, alignment=Qt.AlignHCenter)
        layout.addWidget(title, alignment=Qt.AlignHCenter)
        layout.addWidget(description, alignment=Qt.AlignHCenter)
        layout.addStretch()

        self.setContentsMargins(0, 0, 0, 0)
