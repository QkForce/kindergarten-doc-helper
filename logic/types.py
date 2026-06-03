from enum import Enum, auto
from dataclasses import dataclass
from typing import Callable
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
