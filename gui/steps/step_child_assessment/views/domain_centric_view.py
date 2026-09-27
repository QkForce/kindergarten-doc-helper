from PySide6.QtWidgets import QVBoxLayout, QFrame

from .base_view import BaseView
from ..components.domain_selector import DomainSelector
from logic.types import AssessmentStatus


class DomainCentricView(BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("domain_centric_view_widget")
        # children_scores = [{"name": "Child 1", "code-1": 2, "code-2": 3}, ...]
        self.children_scores = {}

        self.selector = DomainSelector(parent=self)
        self.selector.domainSelected.connect(self.handle_domain_selection)

        empty_frame = QFrame()
        # self.assessment_area.on_score_updated.connect(self.handle_score_update)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.selector)
        layout.addWidget(empty_frame, 1)

    def get_assessment_status(self, children_scores, dom_id) -> AssessmentStatus:
        total_metrics = 0
        scored_metrics = 0
        for scores in children_scores.values():
            dom = scores.get(dom_id)
            if not dom:
                continue
            for sub in dom["subjects"].values():
                for metric in sub["metrics"].values():
                    total_metrics += 1
                    if metric["score"] != 0:
                        scored_metrics += 1

        if scored_metrics == 0:
            return AssessmentStatus.NOT_STARTED
        elif scored_metrics < total_metrics:
            return AssessmentStatus.IN_PROGRESS
        else:
            return AssessmentStatus.COMPLETED

    def get_selector_data(
        self, children_scores
    ) -> list[tuple[str, str, AssessmentStatus]]:
        domain_ids = set()
        for scores in children_scores.values():
            for dom_id, dom in scores.items():
                domain_ids.add((dom_id, dom["name"]))
        return [
            (dom_id, dom_name, self.get_assessment_status(children_scores, dom_id))
            for dom_id, dom_name in domain_ids
        ]

    def applyData(self, children_scores):
        self.children_scores = children_scores
        selector_data = self.get_selector_data(self.children_scores)
        self.selector.applyData(selector_data)
        first_dom_id = selector_data[0][0] if selector_data else None
        if first_dom_id:
            self.selector.selectDomain(first_dom_id)

    def handle_domain_selection(self, dom_id):
        pass  # TODO: Implement domain selection handling for domain-centric view

    def handle_score_update(self, dom_id, scoring_dict):
        pass  # TODO: Implement score update handling for domain-centric view
