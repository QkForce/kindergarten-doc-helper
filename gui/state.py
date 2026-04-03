from typing import Dict, List, Optional
from openpyxl.workbook.workbook import Workbook

from logic.types import AgeGroup
from logic.config_tools import get_age_group_data, get_all_metric_codes


class ChecklistBaseState:
    def __init__(self):
        self.init()

    def init(self):
        self.file_path: str = ""
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

    def reset(self):
        self.init()

    @property
    def age_group_data(self):
        # domain_name: {subject_name: {metric_code: {original: str, transformed: str}}}
        return get_age_group_data(self.age_group)

    @property
    def metric_codes(self):
        # [metric_code1, metric_code2, ...]
        return get_all_metric_codes(self.age_group)


class GeneratorState(ChecklistBaseState):
    def __init__(self):
        super().__init__()
        self.temp_file_path = None


class FillerState(ChecklistBaseState):
    def __init__(self):
        super().__init__()
        self.temp_file_path = None
        self.control_type = None


class SmartEntryState(ChecklistBaseState):
    def __init__(self):
        super().__init__()
        self.children_scores: Dict[str, dict[str, dict[str, dict[str, int | None]]]] = (
            {}
        )
