from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

from gui.widgets.score_toggle import ScoreToggle


class MetricItem(QFrame):
    def __init__(self, metric_name: str):
        super().__init__()
        self.metric_name = metric_name
        self.setObjectName("metric_item")

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameStyle(QFrame.Shape.NoFrame)

        title = QLabel(self.metric_name)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_toggle = ScoreToggle(size=14, spacing=2)
        score_toggle.setObjectName("metric_score_toggle")

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(score_toggle)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)
