from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Signal

from gui.widgets.child_selector import ChildSelector
from gui.widgets.assessment_area import AssessmentArea
from logic.assessment_tools import get_assessment_status


class ChildrenAssessmentWidget(QWidget):
    on_scores_updated = Signal(dict)  # child_name -> score_dict

    def __init__(self):
        super().__init__()
        self.children_scores = {}
        layout = QHBoxLayout(self)

        self.selector = ChildSelector()
        self.selector.childSelected.connect(self.load_child_scores)

        self.assessment_area = AssessmentArea()
        self.assessment_area.on_score_updated.connect(self.handle_score_update)

        layout.addWidget(self.selector)
        layout.addWidget(self.assessment_area, 1)

        self.setContentsMargins(0, 0, 0, 0)

    def applyData(self, children_scores):
        self.children_scores = children_scores
        self.selector.set_data(list(children_scores.keys()))

    def load_child_scores(self, name):
        self.assessment_area.applyChildData(name, self.children_scores.get(name, {}))

    def handle_score_update(self, child_name, scoring_dict):
        self.children_scores[child_name] = scoring_dict
        assessment_status = get_assessment_status(scoring_dict)
        self.selector.setChildStatus(child_name, assessment_status)
