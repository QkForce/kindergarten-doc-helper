from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal

from gui.widgets.score_toggle import ScoreToggle, ScoreButtonType
from gui.utils.formatter import format_criterion_tooltip


class MetricItem(QFrame):
    on_score_updated = Signal(str, int)  # metric_name, score

    def __init__(
        self, metric_name: str, description: str, criteria: list, score: int = 0
    ):
        super().__init__()
        self.metric_name = metric_name
        self.description = description
        self.criteria = [
            format_criterion_tooltip(i, desc)
            for i, desc in enumerate(criteria, start=1)
        ]
        self.setObjectName("metric_item")

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameStyle(QFrame.Shape.NoFrame)

        title = QLabel(self.metric_name)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setToolTip(self.description)

        self.score_toggle = ScoreToggle(
            btn_tooltips=self.criteria,
            btn_type=ScoreButtonType.BASE,
            size=14,
            spacing=2,
        )
        self.score_toggle.set_score(score)
        self.score_toggle.setObjectName("metric_score_toggle")
        self.score_toggle.scoreChanged.connect(
            lambda score: self.on_score_updated.emit(self.metric_name, score)
        )

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.score_toggle)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)

    def applyData(self, score):
        self.score_toggle.set_score(score)
