from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QButtonGroup,
    QPushButton,
)
from PySide6.QtCore import Signal


class ScoreToggle(QWidget):
    scoreChanged = Signal(int)

    def __init__(self, size=24, spacing=4, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.group = QButtonGroup(self)
        self.buttons = {}

        for val in [1, 2, 3]:
            btn = QPushButton(str(val))
            btn.setFixedSize(size, size)
            btn.setCheckable(True)
            btn.setObjectName(f"score_btn_{val}")

            self.group.addButton(btn, val)
            self.layout.addWidget(btn)
            self.buttons[val] = btn

        self.group.idClicked.connect(self.scoreChanged.emit)
