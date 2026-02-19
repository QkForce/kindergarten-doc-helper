from PySide6.QtWidgets import QWidget
from gui.state import BaseState


class StepWidget(QWidget):
    def __init__(self, state: BaseState, parent=None):
        super().__init__(parent)
        self.state = state
        self.title = "title"
        self.description = "description"
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
