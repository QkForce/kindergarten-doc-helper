from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Qt
from gui.widgets.spinner import Spinner


class LoadingPlug(QWidget):
    def __init__(self, title="title", description="description"):
        super().__init__()
        self.title = title
        self.description = description

        spinner = Spinner()
        spinner.setFixedWidth(72)
        spinner.setFixedHeight(72)
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
