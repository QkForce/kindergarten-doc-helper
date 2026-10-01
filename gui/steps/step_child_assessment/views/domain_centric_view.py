from PySide6.QtWidgets import QHBoxLayout


from .base_view import BaseView
from ..components.left_bar_selector import LeftBarSelector
from ..components.domain_assessment_area import DomainAssessmentArea
from logic.assessment_tools import get_assessment_status
from logic.types import (
    AssessmentStatus,
    ChildrenAssessmentDTO,
    DomainCentricAssessmentDTO,
    DomainID,
    SelectorItemDTO,
)


class DomainCentricView(BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("domain_centric_view_widget")
        self.children_scores: ChildrenAssessmentDTO = {}

        self.selector = LeftBarSelector(title="Даму бағытын таңдаңыз:", parent=self)
        self.selector.itemSelected.connect(self.handle_domain_selection)

        self.assessment_area = DomainAssessmentArea(parent=self)
        self.assessment_area.on_score_updated.connect(self.handle_score_update)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.selector)
        layout.addWidget(self.assessment_area, 1)

    def _get_assessment_status(self, dom_id: DomainID) -> AssessmentStatus:
        total_metrics = 0
        scored_metrics = 0
        for scores in self.children_scores.values():
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

    def _get_selector_data(self) -> list[SelectorItemDTO]:
        domain_ids = set()
        for scores in self.children_scores.values():
            for dom_id, dom in scores.items():
                domain_ids.add((dom_id, dom["name"]))
        return [
            SelectorItemDTO(
                id=dom_id,
                title=dom_name,
                status=self._get_assessment_status(dom_id),
            )
            for dom_id, dom_name in domain_ids
        ]

    def _get_assessment_area_data(
        self, dom_id: DomainID
    ) -> tuple[str, DomainCentricAssessmentDTO]:
        dom_name = ""
        domain_data: DomainCentricAssessmentDTO = {}

        for child_name, child_scores in self.children_scores.items():
            if dom_id in child_scores:
                if not dom_name:
                    dom_name = child_scores[dom_id]["name"]
                domain_data[child_name] = child_scores[dom_id]

        return dom_name, domain_data

    def applyData(self, children_scores: ChildrenAssessmentDTO):
        self.children_scores = children_scores
        selector_data = self._get_selector_data()
        self.selector.applyData(selector_data)
        first_dom_id = selector_data[0]["id"] if selector_data else None
        if first_dom_id:
            self.selector.selectItem(first_dom_id)

    def handle_domain_selection(self, dom_id):
        dom_name, dom_data = self._get_assessment_area_data(dom_id)
        self.assessment_area.applyData(dom_id, dom_name, dom_data)

    def handle_score_update(
        self, dom_id: DomainID, scoring_dict: DomainCentricAssessmentDTO
    ):
        pass  # TODO: Implement score update handling for domain-centric view
