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
from logic.assessment_tools import bulk_update, get_common_score_type


class AssessmentArea(QFrame):
    on_score_updated = Signal(str, dict)  # child_name, score_dict
    child_name = ""
    score_dict = {}
    domain_blocks = {}

    def __init__(self):
        super().__init__()
        self.setObjectName("assessment_area")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.child_name_lbl = QLabel()
        self.child_name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.score_toggle = ScoreToggle(size=20, spacing=2)
        self.score_toggle.scoreChanged.connect(self.on_bulk_score)

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

    def on_bulk_score(self, score):
        bulk_update(self.score_dict, score)
        for dn, domain_block in self.domain_blocks.items():
            domain_block.applyData(self.score_dict[dn])
        self.on_score_updated.emit(self.child_name, self.score_dict)

    def handle_child_update(self, dn, subjects):
        # Update self.score_togle state
        self.score_dict[dn] = subjects
        cmn_score = get_common_score_type(self.score_dict)
        self.score_toggle.set_score(cmn_score)
        # Send signal to parent
        self.on_score_updated.emit(self.child_name, self.score_dict)

    def applyChildData(self, child_name, score_dict):
        if child_name is None or score_dict is None:
            return

        self.child_name = child_name
        self.score_dict = score_dict

        self.child_name_lbl.setText(self.child_name)

        # Clear existing domain blocks
        while self.body_layout.count():
            item = self.body_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new domain blocks based on score_dict
        for domain_name, subjects in self.score_dict.items():
            domain_block = DomainBlock(domain_name, subjects)
            domain_block.on_score_updated.connect(self.handle_child_update)
            self.domain_blocks[domain_name] = domain_block
            self.body_layout.addWidget(domain_block)
