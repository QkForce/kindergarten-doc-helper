from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

from gui.widgets.child_selector import ChildSelector
from gui.widgets.items.child_item import AssessmentStatus
from gui.widgets.assessment_area import AssessmentArea


class ChildrenAssessmentWidget(QWidget):
    children_scoring_dict = {}

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.selector = ChildSelector()
        self.selector.childSelected.connect(self.load_child_scores)

        self.assessment_area = AssessmentArea()
        self.assessment_area.on_score_updated.connect(self.handle_score_update)

        layout.addWidget(self.selector)
        layout.addWidget(self.assessment_area, 1)

        self.setContentsMargins(0, 0, 0, 0)

    def set_data(self, children_scoring_dict):
        self.children_scoring_dict = children_scoring_dict
        self.selector.set_data(list(children_scoring_dict.keys()))

    def load_child_scores(self, name):
        self.assessment_area.applyChildData(name, self.children_scoring_dict.get(name, {}))

    def handle_score_update(self, child_name, scoring_dict):
        self.children_scoring_dict[child_name] = scoring_dict
        self.selector.setChildStatus(child_name, AssessmentStatus.COMPLETED)
