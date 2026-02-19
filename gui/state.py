from enum import Enum
from typing import Dict, List, Optional
from openpyxl.workbook.workbook import Workbook


class AgeGroup(Enum):
    EARLY_AGE = "early_age"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    PRESCHOOL = "preschool"


class ChecklistBaseState:
    def __init__(self):
        self.workbook: Optional[Workbook] = None
        self.sheet_name: str = ""
        self.age_group: Optional[AgeGroup] = None

        # Data Location in Excel (Coordinates)
        self.children_start_row: int = 0
        self.children_end_row: int = 0
        self.children_col: int = 0
        self.metric_code_row: int = 0
        self.metric_desc_row: int = 0
        self.metric_start_col: int = 0
        self.metric_end_col: int = 0

        # Main Data
        self.source_metrics: List[Dict[str, str]] = []
        self.children_scores: List[dict] = []


class GeneratorState(ChecklistBaseState):
    def __init__(self):
        super().__init__()
