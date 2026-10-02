from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from gui.constants.icons import IconPaths
from gui.constants.colors import AppColors
from gui.steps.step_child_assessment.components.subject_block import SubjectBlock
from gui.utils.icon_utils import get_svg_pixmap
from gui.widgets.rotating_icon import RotatingIcon
from gui.widgets.score_toggle import ScoreButtonType, ScoreToggle
from logic.assessment_tools import get_domain_score_type, set_subjects_score
from logic.types import ChildName, DomainScoreDTO, SubjectID, SubjectScoreDTO


class DomainChildBlock(QFrame):
    on_score_updated = Signal(str, dict)  # (child_name, updated_domain_score)

    def __init__(
        self,
        child_name: ChildName,
        domain_score: DomainScoreDTO,
        is_expanded=False,
        parent=None,
    ):
        super().__init__(parent)
        self.child_name: ChildName = child_name
        self.domain_score: DomainScoreDTO = domain_score
        self.is_expanded: bool = is_expanded
        self.subjects: dict[SubjectID, SubjectScoreDTO] = domain_score["subjects"]
        self.subject_blocks: dict[SubjectID, SubjectBlock] = {}

        self.setObjectName("domain_child_block")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self._setup_ui()

    def _setup_ui(self):
        pixmap = get_svg_pixmap(IconPaths.CHEVRON_DOWN, AppColors.ICON_MAIN, 16)
        self.chevron_icon = RotatingIcon(
            pixmap, 0 if self.is_expanded else -90, parent=self
        )
        self.chevron_icon.setFixedSize(16, 16)

        title = QLabel(self.child_name)
        title.setProperty("lbl-level", "h3")

        self.score_toggle = ScoreToggle(
            btn_type=ScoreButtonType.BASE,
            spacing=4,
            parent=self,
        )
        current_common_score = get_domain_score_type(self.subjects)
        self.score_toggle.blockSignals(True)
        self.score_toggle.set_score(current_common_score)
        self.score_toggle.blockSignals(False)
        self.score_toggle.scoreChanged.connect(self._on_bulk_score)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.chevron_icon)
        header_layout.addSpacing(4)
        header_layout.addWidget(title, stretch=1)
        header_layout.addWidget(self.score_toggle)

        self.line = QFrame(self)
        self.line.setObjectName("separator")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setVisible(self.is_expanded)

        body_layout = QVBoxLayout()
        body_layout.setSpacing(8)
        for sub_id, sub in self.subjects.items():
            subject_block = SubjectBlock(
                sub_id, sub, is_expanded=self.is_expanded, parent=self
            )
            subject_block.on_score_updated.connect(self._handle_subject_update)
            self.subject_blocks[sub_id] = subject_block
            subject_block.setVisible(self.is_expanded)
            body_layout.addWidget(subject_block)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        layout.addLayout(header_layout)
        layout.addWidget(self.line)
        layout.addLayout(body_layout)

    def mousePressEvent(self, event):
        self.setExpanded(not self.is_expanded)
        super().mousePressEvent(event)

    def setExpanded(self, expanded: bool):
        self.is_expanded = expanded
        self.chevron_icon.rotate(0 if self.is_expanded else -90)
        self.line.setVisible(expanded)
        for sub_block in self.subject_blocks.values():
            sub_block.setExpanded(expanded)
            sub_block.setVisible(expanded)

    def _handle_subject_update(self, sub_id: SubjectID, updated_metrics: dict):
        self.subjects[sub_id]["metrics"] = updated_metrics
        self.domain_score["subjects"] = self.subjects

        # Ортақ баға индикаторын жыпылықтатпай жаңарту
        current_common_score = get_domain_score_type(self.subjects)
        self.score_toggle.blockSignals(True)
        self.score_toggle.set_score(current_common_score)
        self.score_toggle.blockSignals(False)

        self.on_score_updated.emit(self.child_name, self.domain_score)

    def _on_bulk_score(self, score: int):
        set_subjects_score(self.subjects, score)
        self.domain_score["subjects"] = self.subjects
        for sub_id, sub in self.subjects.items():
            self.subject_blocks[sub_id].applyData(sub["metrics"])

        # self.id емес, self.child_name және self.domain_score!
        self.on_score_updated.emit(self.child_name, self.domain_score)

    def applyData(self, domain_score: DomainScoreDTO):
        self.domain_score = domain_score
        self.subjects = domain_score["subjects"]
        for sub_id, sub in self.subjects.items():
            if sub_id in self.subject_blocks:
                self.subject_blocks[sub_id].applyData(sub["metrics"])

        current_common_score = get_domain_score_type(self.subjects)
        self.score_toggle.blockSignals(True)
        self.score_toggle.set_score(current_common_score)
        self.score_toggle.blockSignals(False)
