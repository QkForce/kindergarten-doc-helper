from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Signal

from gui.widgets.rotating_icon import RotatingIcon
from gui.widgets.score_toggle import ScoreToggle, ScoreButtonType
from gui.widgets.assessment.metric_item import MetricItem
from gui.constants.icons import IconPaths
from gui.constants.colors import AppColors
from gui.utils.icon_utils import get_svg_pixmap
from logic.assessment_tools import set_metrics_score, get_subject_score_type


class SubjectBlock(QFrame):
    on_score_updated = Signal(str, dict)  # sub_id, metrics

    def __init__(
        self, id: str, name: str, metrics: dict, is_expanded=False, parent=None
    ):
        super().__init__(parent)
        self.id = id
        self.name = name
        self.metrics = metrics
        self.metric_items = {}
        self.is_expanded = is_expanded
        self.setObjectName("subject_block")
        layout = QVBoxLayout(self)

        title = QLabel(self.name)
        pixmap = get_svg_pixmap(IconPaths.CHEVRON_DOWN, AppColors.ICON_MAIN, 16)
        self.chevron_icon = RotatingIcon(pixmap, -90)
        self.line = QFrame()
        self.line.setObjectName("separator")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.score_toggle = ScoreToggle(
            btn_type=ScoreButtonType.BASE, size=16, spacing=2, parent=self
        )
        self.score_toggle.setObjectName("subject_score_toggle")
        self.score_toggle.scoreChanged.connect(self.on_bulk_score)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.chevron_icon)
        header_layout.addSpacing(4)
        header_layout.addWidget(title, stretch=1)
        header_layout.addWidget(self.score_toggle)

        self.body_frame = QFrame(parent=self)
        body_layout = QHBoxLayout(self.body_frame)
        for i, (met_id, met) in enumerate(self.metrics.items()):
            metric_item = MetricItem(
                id=met_id,
                code=met["code"],
                description=met["description"],
                criteria=met["criteria"],
                parent=self.body_frame,
            )
            metric_item.on_score_updated.connect(self.handle_child_update)
            self.metric_items[met_id] = metric_item
            body_layout.addWidget(metric_item)
            if i < len(self.metrics) - 1:
                body_layout.addStretch(1)

        self.line.setVisible(self.is_expanded)
        self.body_frame.setVisible(self.is_expanded)
        self.applyData(self.metrics)

        layout.addLayout(header_layout)
        layout.addWidget(self.line)
        layout.addWidget(self.body_frame, stretch=1)
        layout.addStretch(1)

    def mousePressEvent(self, event):
        self.setExpanded(not self.is_expanded)
        super().mousePressEvent(event)

    def setExpanded(self, is_expanded):
        self.is_expanded = is_expanded
        target_angle = 0 if self.is_expanded else -90
        self.chevron_icon.rotate(target_angle)
        self.line.setVisible(self.is_expanded)
        self.body_frame.setVisible(self.is_expanded)

    def on_bulk_score(self, score):
        set_metrics_score(self.metrics, score)
        for mn, metric in self.metrics.items():
            self.metric_items[mn].applyData(metric["score"])
        # Send signal to parent (isn't necessary to send again)
        self.on_score_updated.emit(self.id, self.metrics)
        # It is not necessary to update the score_toggle state here
        # because it called this method, so its state is already up to date.

    def handle_child_update(self, met_id, score):
        self.metrics[met_id] = {
            "score": score,
            "description": self.metrics[met_id]["description"],
            "criteria": self.metrics[met_id]["criteria"],
        }
        cmn_score = get_subject_score_type(self.metrics)
        self.score_toggle.set_score(cmn_score)
        self.on_score_updated.emit(self.id, self.metrics)

    def applyData(self, metrics):
        self.metrics = metrics
        for met_id, met in self.metrics.items():
            self.metric_items[met_id].applyData(met["score"])
        cmn_score = get_subject_score_type(self.metrics)
        self.score_toggle.set_score(cmn_score)
