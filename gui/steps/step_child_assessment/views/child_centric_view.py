from PySide6.QtWidgets import QHBoxLayout

from .base_view import BaseView
from ..components.child_selector import ChildSelector
from ..components.child_assessment_area import ChildAssessmentArea
from logic.assessment_tools import get_assessment_status
from logic.types import ChildrenAssessmentDTO


class ChildCentricView(BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("child_centric_view_widget")
        self.children_scores: ChildrenAssessmentDTO = {}

        self.selector = ChildSelector(parent=self)
        self.selector.childSelected.connect(self.handle_child_selection)

        self.assessment_area = ChildAssessmentArea(parent=self)
        self.assessment_area.on_score_updated.connect(self.handle_score_update)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.selector)
        layout.addWidget(self.assessment_area, 1)

    def applyData(self, children_scores: ChildrenAssessmentDTO):
        self.children_scores = children_scores
        selector_data = [
            (name, get_assessment_status(scores))
            for name, scores in children_scores.items()
        ]
        self.selector.applyData(selector_data)
        first_child_name = selector_data[0][0] if selector_data else None
        if first_child_name:
            self.selector.selectChild(first_child_name)

    def handle_child_selection(self, name: str):
        self.assessment_area.applyChildData(name, self.children_scores[name])

    def handle_score_update(self, child_name: str, scoring_dict: dict):
        self.children_scores[child_name] = scoring_dict
        assessment_status = get_assessment_status(scoring_dict)
        self.selector.setChildStatus(child_name, assessment_status)
        self.on_scores_updated.emit(self.children_scores)
