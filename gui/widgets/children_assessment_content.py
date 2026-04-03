from PySide6.QtWidgets import QFrame, QHBoxLayout
from PySide6.QtCore import Signal

from gui.widgets.child_selector import ChildSelector
from gui.widgets.assessment_area import AssessmentArea
from logic.assessment_tools import get_assessment_status


class ChildrenAssessmentWidget(QFrame):
    on_scores_updated = Signal(dict)  # child_name -> score_dict

    def __init__(self):
        super().__init__()
        # children_scores = [{"name": "Child 1", "code-1": 2, "code-2": 3}, ...]
        self.children_scores = {}
        self.setObjectName("children_assessment_widget")

        self.selector = ChildSelector()
        self.selector.childSelected.connect(self.handle_child_selection)

        self.assessment_area = AssessmentArea()
        self.assessment_area.on_score_updated.connect(self.handle_score_update)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.selector)
        layout.addWidget(self.assessment_area, 1)

    def applyData(self, children_scores):
        self.children_scores = children_scores
        selector_data = [
            (name, get_assessment_status(scores))
            for name, scores in children_scores.items()
        ]
        self.selector.applyData(selector_data)
        first_child_name = selector_data[0][0] if selector_data else None
        if first_child_name:
            self.selector.selectChild(first_child_name)

    def handle_child_selection(self, name):
        self.assessment_area.applyChildData(name, self.children_scores[name])

    def handle_score_update(self, child_name, scoring_dict):
        self.children_scores[child_name] = scoring_dict
        assessment_status = get_assessment_status(scoring_dict)
        self.selector.setChildStatus(child_name, assessment_status)
        self.on_scores_updated.emit(self.children_scores)
