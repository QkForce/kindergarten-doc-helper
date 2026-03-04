from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)

from gui.widgets.score_toggle import ScoreToggle
from gui.widgets.assessment.metric_item import MetricItem


class SubjectBlock(QFrame):
    def __init__(self, subject_name: str, metrics: dict):
        super().__init__()
        self.subject_name = subject_name
        self.metrics = metrics
        self.setObjectName("subject_block")
        layout = QVBoxLayout(self)

        title = QLabel(self.subject_name)
        line = QFrame()
        line.setObjectName("separator")
        line.setFrameShape(QFrame.Shape.HLine)
        score_toggle = ScoreToggle(size=16, spacing=2)
        score_toggle.setObjectName("subject_score_toggle")

        header_layout = QHBoxLayout()
        header_layout.addWidget(title, stretch=1)
        header_layout.addWidget(score_toggle)

        body_layout = QHBoxLayout()
        for i, metric_name in enumerate(self.metrics.keys()):
            body_layout.addWidget(MetricItem(metric_name=metric_name))
            if i < len(self.metrics) - 1:
                body_layout.addStretch(1)

        layout.addLayout(header_layout)
        layout.addWidget(line)
        layout.addLayout(body_layout, stretch=1)
        layout.addStretch(1)
