from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.steps.common.step_children_scores import StepChildrenScores
from gui.steps.filler.step_docx_fill import StepDocxFill
from gui.widgets.wizard_widget import WizardWidget
from gui.state import FillerState


class FillerPage(WizardWidget[FillerState]):
    def __init__(self, on_finish: Callable):
        state = FillerState()
        step_factories = [
            lambda: StepFileSelect(state),
            lambda: StepChildrenScores(state),
            lambda: StepDocxFill(state),
        ]
        super().__init__(
            step_factories=step_factories, state=state, on_finish=on_finish
        )
