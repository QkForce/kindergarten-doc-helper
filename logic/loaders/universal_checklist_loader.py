from logic.loaders.children_loader import ChildrenLoader
from logic.loaders.metrics_loader import MetricsLoader
from logic.loaders.scores_loader import ScoresLoader


class UniversalChecklistLoader:
    def __init__(self, sheet):
        self.sheet = sheet
        self.children_loader = ChildrenLoader(sheet)
        self.metrics_loader = MetricsLoader(sheet)
        self.scores_loader = ScoresLoader(sheet)

    def load_auto(self):
        # 1. Finding children
        c_res = self.children_loader.load_auto()
        children, c_start, c_end, c_col = c_res

        # 2. Finding metrics
        m_res = self.metrics_loader.load_auto()
        metrics, m_code_row, m_desc_row, m_start_col, m_end_col = m_res

        # 3. Download Scores
        metric_codes = [m["code"] for m in metrics]
        scores = self.scores_loader.load_manual(
            c_start, c_end, c_col, m_start_col, metric_codes
        )

        return {
            "children_data": (c_start, c_end, c_col),
            "metrics_data": (metrics, m_code_row, m_desc_row, m_start_col, m_end_col),
            "children_scores": scores,
        }
