from typing import TypeVar, Generic
from PySide6.QtWidgets import QWidget, QVBoxLayout

T = TypeVar("T")


class BaseStep(QWidget, Generic[T]):
    def __init__(self, state: T, parent=None):
        super().__init__(parent)
        self.state = state
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setup_ui()
        self.setup_state_machine()
        self.connect_signals()

    def setup_ui(self):
        raise NotImplementedError("setup_ui must be implemented")

    def setup_state_machine(self):
        raise NotImplementedError()

    def connect_signals(self):
        raise NotImplementedError()

    def run_auto_load(self):
        raise NotImplementedError()

    def validate_before_next(self) -> bool:
        raise NotImplementedError()
