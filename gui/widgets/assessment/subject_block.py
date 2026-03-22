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
from gui.constants.strings import SUBJECT_NAMES
from gui.constants.icons import IconPaths
from gui.constants.colors import AppColors
from gui.utils.icon_utils import get_svg_pixmap
from logic.assessment_tools import set_metrics_score, get_subject_score_type


class SubjectBlock(QFrame):
    on_score_updated = Signal(str, dict)  # subject_name, metrics

    def __init__(self, subject_name: str, metrics: dict):
        super().__init__()
        self.subject_name = subject_name
        self.metrics = metrics
        self.metric_items = {}
        self.is_expanded = True
        self.setObjectName("subject_block")
        layout = QVBoxLayout(self)

        title = QLabel(SUBJECT_NAMES.get(self.subject_name, self.subject_name))
        pixmap = get_svg_pixmap(IconPaths.CHEVRON_DOWN, AppColors.ICON_MAIN, 16)
        self.chevron_icon = RotatingIcon(pixmap)
        line = QFrame()
        line.setObjectName("separator")
        line.setFrameShape(QFrame.Shape.HLine)
        self.score_toggle = ScoreToggle(
            btn_type=ScoreButtonType.BASE, size=16, spacing=2
        )
        self.score_toggle.setObjectName("subject_score_toggle")
        self.score_toggle.scoreChanged.connect(self.on_bulk_score)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.chevron_icon)
        header_layout.addSpacing(4)
        header_layout.addWidget(title, stretch=1)
        header_layout.addWidget(self.score_toggle)

        body_layout = QHBoxLayout()
        for i, mn in enumerate(self.metrics.keys()):
            metric_item = MetricItem(metric_name=mn)
            metric_item.on_score_updated.connect(self.handle_child_update)
            self.metric_items[mn] = metric_item
            body_layout.addWidget(metric_item)
            if i < len(self.metrics) - 1:
                body_layout.addStretch(1)

        layout.addLayout(header_layout)
        layout.addWidget(line)
        layout.addLayout(body_layout, stretch=1)
        layout.addStretch(1)

    def mousePressEvent(self, event):
        self.toggle_expand()
        super().mousePressEvent(event)

    def toggle_expand(self):
        self.is_expanded = not self.is_expanded
        target_angle = 0 if self.is_expanded else -90
        self.chevron_icon.rotate(target_angle)
        print(f"Status: {'Expanded' if self.is_expanded else 'Collapsed'}")

    def on_bulk_score(self, score):
        set_metrics_score(self.metrics, score)
        for mn, score in self.metrics.items():
            self.metric_items[mn].applyData(score)
        # Send signal to parent (isn't necessary to send again)
        self.on_score_updated.emit(self.subject_name, self.metrics)
        # It is not necessary to update the score_toggle state here
        # because it called this method, so its state is already up to date.

    def handle_child_update(self, metric_name, score):
        self.metrics[metric_name] = score
        cmn_score = get_subject_score_type(self.metrics)
        self.score_toggle.set_score(cmn_score)
        self.on_score_updated.emit(self.subject_name, self.metrics)

    def applyData(self, metrics):
        self.metrics = metrics
        for mn, score in self.metrics.items():
            self.metric_items[mn].applyData(score)
        cmn_score = get_subject_score_type(self.metrics)
        self.score_toggle.set_score(cmn_score)
