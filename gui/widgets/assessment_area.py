from PySide6.QtWidgets import (
    QFrame,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)
from PySide6.QtCore import Qt, Signal

from gui.widgets.score_toggle import ScoreToggle
from gui.widgets.assessment.domain_block import DomainBlock
from logic.assessment_tools import set_score


class AssessmentArea(QFrame):
    on_score_updated = Signal(str, dict)
    child_name = ""
    scoring_dict = {}

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.child_name_lbl = QLabel()
        self.child_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.score_toggle = ScoreToggle(size=20, spacing=2)
        self.score_toggle.scoreChanged.connect(self.handle_score_change)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.child_name_lbl, stretch=1)
        header_layout.addWidget(self.score_toggle)

        # Create a ScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Create a custom widget for your content
        self.scroll_content = QWidget()
        self.body_layout = QVBoxLayout(self.scroll_content)
        self.body_layout.setAlignment(Qt.AlignTop)

        # Setting content to ScrollArea
        self.scroll_area.setWidget(self.scroll_content)

        # Add to main layout
        layout.addLayout(header_layout)
        layout.addWidget(self.scroll_area)

        self.update_ui()

    def update_ui(self):
        self.child_name_lbl.setText(self.child_name)

        # Clear existing domain blocks
        while self.body_layout.count():
            item = self.body_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new domain blocks based on scoring_dict
        for domain_name, subjects in self.scoring_dict.items():
            domain_block = DomainBlock(domain_name, subjects)
            self.body_layout.addWidget(domain_block)

        # Fill remaining space
        self.body_layout.addStretch()

    def handle_score_change(self, score):
        set_score(self.scoring_dict, score=score)
        self.on_score_updated.emit(self.child_name, self.scoring_dict)

    def updateChild(self, child_name, scoring_dict):
        self.child_name = child_name
        self.scoring_dict = scoring_dict
        self.update_ui()
