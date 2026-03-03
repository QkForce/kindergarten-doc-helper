from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

from gui.widgets.child_selector import ChildSelector
from gui.widgets.assessment_area import AssessmentArea


class ChildrenAssessmentWidget(QWidget):
    children_scoring_dict = {}

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)

        self.selector = ChildSelector()
        self.selector.childSelected.connect(self.load_child_scores)

        self.assessment_area = AssessmentArea()
        self.assessment_area.setAlignment(Qt.AlignCenter)
        self.assessment_area.on_score_updated.connect(self.handle_score_update)

        layout.addWidget(self.selector)
        layout.addWidget(self.assessment_area, 1)

        self.setContentsMargins(0, 0, 0, 0)

    def set_data(self, children_names):
        self.selector.set_data(children_names)

    def load_child_scores(self, name):
        self.assessment_area.updateChild(name, {})

    def handle_score_update(self, child_name, scoring_dict):
        self.children_scoring_dict[child_name] = scoring_dict
        print(f"Updated scores for {child_name}: {scoring_dict}")
