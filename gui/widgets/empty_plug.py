from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class EmptyPlug(QWidget):
    def __init__(self, title, description):
        super().__init__()
        self.title = title
        self.description = description

        icon_lbl = QLabel()
        icon_pixmap = QPixmap("gui\\resources\\icons\\draft.png")
        icon_lbl.setPixmap(icon_pixmap)

        title_lbl = QLabel(self.title)
        title_lbl.setProperty("lbl-level", "h2")
        # title_lbl.setWordWrap(True)

        description_lbl = QLabel(self.description)
        description_lbl.setProperty("lbl-level", "h3-normal")
        # description_lbl.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addWidget(icon_lbl, alignment=Qt.AlignCenter)
        layout.addWidget(title_lbl, alignment=Qt.AlignCenter)
        layout.addWidget(description_lbl, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setContentsMargins(0, 0, 0, 0)
