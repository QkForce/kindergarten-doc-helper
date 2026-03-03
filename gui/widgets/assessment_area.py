from PySide6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal

from gui.widgets.score_toggle import ScoreToggle
from logic.assessment_tools import set_score


class AssessmentArea(QScrollArea):
    on_score_updated = Signal(str, dict)
    child_name = ""
    scoring_dict = {}

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        self.child_name_lbl = QLabel()
        self.child_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.score_toggle = ScoreToggle(size=20, spacing=2)
        self.score_toggle.scoreChanged.connect(self.handle_score_change)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.child_name_lbl, stretch=1)
        header_layout.addWidget(self.score_toggle)

        main_layout = QVBoxLayout()

        layout.addLayout(header_layout)
        layout.addLayout(main_layout, stretch=1)
        layout.addStretch(1)

    def update_ui(self):
        self.child_name_lbl.setText(self.child_name)

    def handle_score_change(self, score):
        set_score(self.scoring_dict, score=score)
        self.on_score_updated.emit(self.child_name, self.scoring_dict)

    def updateChild(self, child_name, scoring_dict):
        self.child_name = child_name
        self.scoring_dict = scoring_dict
        self.update_ui()
