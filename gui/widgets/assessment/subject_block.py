from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel

from gui.widgets.score_toggle import ScoreToggle
from gui.widgets.assessment.metric_item import MetricItem
from gui.widgets.flow_layout import FlowLayout


class SubjectBlock(QFrame):
    def __init__(self, subject_name: str, metrics: dict):
        super().__init__()
        self.subject_name = subject_name
        self.metrics = metrics

        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)

        title = QLabel(self.subject_name)
        score_toggle = ScoreToggle(size=20, spacing=2)

        header_layout = QHBoxLayout()
        header_layout.addWidget(title, stretch=1)
        header_layout.addWidget(score_toggle)

        body_layout = FlowLayout(spacing=5)
        for metric_name in self.metrics.keys():
            body_layout.addWidget(MetricItem(metric_name=metric_name))

        layout.addLayout(header_layout)
        layout.addLayout(body_layout, stretch=1)
        layout.addStretch(1)
