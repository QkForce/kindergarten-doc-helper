from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel

from gui.widgets.score_toggle import ScoreToggle


class MetricItem(QFrame):
    def __init__(self, metric_name: str):
        super().__init__()
        self.metric_name = metric_name

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameStyle(QFrame.Shape.NoFrame)

        title = QLabel(self.metric_name)
        score_toggle = ScoreToggle(size=20, spacing=2)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(score_toggle)
        layout.addStretch(1)
