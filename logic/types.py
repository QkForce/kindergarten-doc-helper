from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, TypedDict
from PySide6.QtWidgets import QWidget


class AssessmentStatus(Enum):
    NOT_STARTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()


@dataclass
class Step:
    title: str
    description: str
    factory: Callable[[], QWidget]


# For IDE hints and easier code reading
ChildName = str
DomainID = str
SubjectID = str
MetricID = str


class MetricScoreDTO(TypedDict):
    code: str
    score: Optional[int]
    description: str
    criteria: List[str]


class SubjectScoreDTO(TypedDict):
    name: str
    metrics: Dict[MetricID, MetricScoreDTO]


class DomainScoreDTO(TypedDict):
    name: str
    subjects: Dict[SubjectID, SubjectScoreDTO]


# ChildName -> DomainID -> DomainScoreDTO
ChildrenAssessmentDTO = Dict[ChildName, Dict[DomainID, DomainScoreDTO]]
