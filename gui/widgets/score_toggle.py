from enum import Enum

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QButtonGroup,
    QPushButton,
)
from PySide6.QtCore import Signal


class ScoreButtonType(Enum):
    BASE = "base"
    DOMAIN = "domain"


class ScoreToggle(QWidget):
    scoreChanged = Signal(int)

    def __init__(self, btn_type=ScoreButtonType.BASE, size=24, spacing=4, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(spacing)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)
        self.buttons = {}
        self.current_score = 0

        for val in [1, 2, 3]:
            btn = QPushButton(str(val))
            btn.setFixedSize(size, size)
            btn.setCheckable(True)
            btn.setObjectName(f"score_btn_{val}")
            btn.setProperty("class", f"score_btn")
            btn.setProperty("mode", btn_type.value)
            btn.clicked.connect(
                lambda checked, score=val: self._on_button_clicked(score)
            )

            self.group.addButton(btn, val)
            self.layout.addWidget(btn)
            self.buttons[val] = btn

    def _on_button_clicked(self, score_id):
        if self.current_score == score_id:
            self.set_score(0)
            self.scoreChanged.emit(0)
        else:
            self.set_score(score_id)
            self.scoreChanged.emit(score_id)

    def set_score(self, score: int):
        self.blockSignals(True)
        try:
            if score in self.buttons:
                btn = self.buttons[score]
                btn.setChecked(True)
                btn.setProperty("score", score)
                btn.style().unpolish(btn)
                btn.style().polish(btn)
                btn.update()
            elif score == 0:
                checked_btn = self.group.checkedButton()
                if checked_btn:
                    self.group.setExclusive(False)
                    checked_btn.setChecked(False)
                    self.group.setExclusive(True)
            self.current_score = score
        finally:
            self.blockSignals(False)

    def get_score(self) -> int:
        return self.current_score
