from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.steps.common.step_children_scores import StepChildrenScores
from gui.steps.filler.step_docx_fill import StepDocxFill
from gui.widgets.wizard_widget import WizardWidget
from gui.state import FillerState
from gui.types import Step
from gui.constants.strings import FILLER_OPTIONS


class FillerPage(WizardWidget[FillerState]):
    def __init__(self, on_finish: Callable):
        state = FillerState()
        step_factories = [
            lambda: StepFileSelect(state),
            lambda: StepChildrenScores(state),
            lambda: StepDocxFill(state),
        ]
        steps = []
        for index, factory in enumerate(step_factories):
            step = Step(
                title=FILLER_OPTIONS[index]["title"],
                description=FILLER_OPTIONS[index]["desc"],
                factory=factory,
            )
            steps.append(step)
        super().__init__(steps=steps, state=state, on_finish=on_finish)
