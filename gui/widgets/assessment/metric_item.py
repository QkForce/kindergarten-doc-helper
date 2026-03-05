from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal

from gui.widgets.score_toggle import ScoreToggle


class MetricItem(QFrame):
    on_score_updated = Signal(int)  # score

    def __init__(self, metric_name: str):
        super().__init__()
        self.metric_name = metric_name
        self.setObjectName("metric_item")

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameStyle(QFrame.Shape.NoFrame)

        title = QLabel(self.metric_name)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_toggle = ScoreToggle(size=14, spacing=2)
        self.score_toggle.setObjectName("metric_score_toggle")
        self.score_toggle.scoreChanged.connect(self.on_score_updated.emit)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.score_toggle)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)

    def applyData(self, score):
        self.score_toggle.set_score(score)
