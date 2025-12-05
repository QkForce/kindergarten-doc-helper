from enum import Enum
from typing import Dict, List
from openpyxl.workbook.workbook import Workbook


class AgeGroup(Enum):
    EARLY_AGE = "early_age"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    PRESCHOOL = "preschool"


class AppState:
    workbook: Workbook = None
    sheet_name: str = ""
    age_group: AgeGroup = None
    children_start_row: int = 0
    children_end_row: int = 0
    children_col: int = 0
    metric_code_row: int = 0
    metric_desc_row: int = 0
    metric_start_col: int = 0
    metric_end_col: int = 0
    source_metrics: List[Dict[str, str]] = None
    age_group_data: Dict[str, Dict[str, Dict]] = None
    children_scores: List[dict] = None
