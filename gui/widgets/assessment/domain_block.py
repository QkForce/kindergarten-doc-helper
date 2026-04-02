from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Signal

from gui.widgets.assessment.subject_block import SubjectBlock
from gui.widgets.score_toggle import ScoreToggle, ScoreButtonType
from gui.utils.assessment_tools import set_subjects_score, get_domain_score_type
from gui.constants.strings import DOMAIN_NAMES
from gui.utils.style_utils import apply_shadow


class DomainBlock(QFrame):
    on_score_updated = Signal(str, dict)  # domain_name, subjects

    def __init__(self, domain_name, subjects):
        super().__init__()
        self.domain_name = domain_name
        self.subjects = subjects
        self.subject_blocks = {}
        self.setObjectName("domain_block")

        self.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 10)
        layout.setSpacing(0)

        title = QLabel(DOMAIN_NAMES.get(self.domain_name, self.domain_name))
        self.score_toggle = ScoreToggle(
            btn_type=ScoreButtonType.DOMAIN, size=18, spacing=2
        )
        self.score_toggle.setObjectName("domain_score_toggle")
        self.score_toggle.scoreChanged.connect(self.on_bulk_score)

        header_widget = QFrame()
        header_widget.setObjectName("domain_header")
        header_widget.setContentsMargins(0, 0, 0, 0)
        header_layout = QHBoxLayout(header_widget)
        header_layout.addWidget(title, stretch=1)
        header_layout.addWidget(self.score_toggle)

        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        for subject_name in self.subjects.keys():
            is_expanded = False
            subject_block = SubjectBlock(
                subject_name, self.subjects[subject_name], is_expanded
            )
            subject_block.on_score_updated.connect(self.handle_child_update)
            self.subject_blocks[subject_name] = subject_block
            body_layout.addWidget(subject_block)
        self.applyData(self.subjects)

        layout.addWidget(header_widget)
        layout.addLayout(body_layout, stretch=1)
        layout.addStretch(1)

        # Shadow
        apply_shadow(self)

    def on_bulk_score(self, score):
        set_subjects_score(self.subjects, score)
        for sn, metrics in self.subjects.items():
            self.subject_blocks[sn].applyData(metrics)
        # Send signal to parent (isn't necessary to send again)
        self.on_score_updated.emit(self.domain_name, self.subjects)
        # It is not necessary to update the score_toggle state here
        # because it called this method, so its state is already up to date.

    def handle_child_update(self, sn, metrics):
        # Update self.score_togle state
        self.subjects[sn] = metrics
        cmn_score = get_domain_score_type(self.subjects)
        self.score_toggle.set_score(cmn_score)
        # Send signal to parent
        self.on_score_updated.emit(self.domain_name, self.subjects)

    def applyData(self, subjects):
        self.subjects = subjects
        for sn, metrics in self.subjects.items():
            self.subject_blocks[sn].applyData(metrics)
        cmn_score = get_domain_score_type(self.subjects)
        self.score_toggle.set_score(cmn_score)
