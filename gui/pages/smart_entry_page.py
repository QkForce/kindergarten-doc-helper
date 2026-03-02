from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.widgets.wizard_widget import WizardWidget
from gui.state import SmartEntryState


class SmartEntryPage(WizardWidget[SmartEntryState]):
    def __init__(self, on_finish: Callable):
        state = SmartEntryState()
        step_factories = [
            lambda: StepFileSelect(state),
        ]
        super().__init__(
            step_factories=step_factories, state=state, on_finish=on_finish
        )
