from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class ScoreCellWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)
