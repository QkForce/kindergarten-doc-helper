from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
)
from PySide6.QtCore import Signal

from .views.child_centric_view import ChildCentricView
from .views.domain_centric_view import DomainCentricView
from gui.widgets.ui.segmented_control import SegmentedControl
from gui.constants.icons import IconPaths


class ChildrenAssessmentContent(QWidget):
    on_scores_updated = Signal(dict)  # child_name -> score_dict

    def __init__(self, parent=None):
        super().__init__(parent)
        # children_scores = [{"name": "Child 1", "code-1": 2, "code-2": 3}, ...]
        self.children_scores = {}
        self.setup_ui()

    def setup_ui(self):
        views_label = QLabel("Көріністер: ", self)
        views_label.setProperty("lbl-level", "h3")
        options = [
            ("Бала бойынша", IconPaths.USERS),
            ("Бағыт бойынша", IconPaths.DOMAINS),
        ]
        self.segmented_control = SegmentedControl(options, default_index=0, parent=self)

        top_bar_frame = QFrame()
        top_bar_frame.setObjectName("top_bar_frame")
        top_bar_layout = QHBoxLayout(top_bar_frame)
        top_bar_layout.setContentsMargins(12, 8, 12, 8)
        top_bar_layout.addWidget(views_label)
        top_bar_layout.addWidget(self.segmented_control)
        top_bar_layout.addStretch()

        self.child_view = ChildCentricView(parent=self)
        self.domain_view = DomainCentricView(parent=self)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.child_view)  # Index 0
        self.stack.addWidget(self.domain_view)  # Index 1

        self.segmented_control.on_option_changed.connect(self._on_mode_changed)
        self.child_view.on_scores_updated.connect(self._on_scores_updated)
        self.domain_view.on_scores_updated.connect(self._on_scores_updated)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(top_bar_frame)
        layout.addSpacing(16)
        layout.addWidget(self.stack, 1)

    def applyData(self, children_scores: dict):
        """Деректер келгенде екі көрініске де береміз."""
        self.children_scores = children_scores
        self.child_view.applyData(self.children_scores)
        self.domain_view.applyData(self.children_scores)

    def _on_mode_changed(self, mode_id: int):
        """Режим ауысқанда соңғы стейтті белсенді view-ға синхрондау."""
        self.stack.setCurrentIndex(mode_id)
        if mode_id == 0:
            self.child_view.applyData(self.children_scores)
        else:
            self.domain_view.applyData(self.children_scores)

    def _on_scores_updated(self, updated_scores: dict):
        self.children_scores = updated_scores
        self.on_scores_updated.emit(self.children_scores)
