from enum import Enum
from typing import Dict, List
from openpyxl.workbook.workbook import Workbook


class AgeGroup(Enum):
    EARLY_AGE = "early_age"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    PRESCHOOL = "preschool"


class MetricType(Enum):
    PHYSICAL = "physical"
    COMMUNICATIVE = "communicative"
    COGNITIVE = "cognitive"
    CREATIVITY = "creativity"
    SOCIAL = "social"


MARKERS_BY_TYPE = {
    "physical": "physical-1",
    "communicative": "communicative-1",
    "cognitive": "cognitive-1",
    "creativity": "creativity-1",
    "social": "social-1",
}


class AppState:
    workbook: Workbook = None
    sheet_name: str = ""
    group_type: AgeGroup = None
    metrics_groups: Dict[str, List[str]] = None
    markers_by_type = MARKERS_BY_TYPE
    children_start_row: int = 0
    children_end_row: int = 0
    children_col: int = 0
    metric_code_row: int = 0
    metric_desc_row: int = 0
    metric_start_col: int = 0
    metric_end_col: int = 0
    source_metrics: List[Dict[str, str]] = None
    metrics_mapping: Dict[str, Dict[str, str]] = None
    children_scores: List[dict] = None
