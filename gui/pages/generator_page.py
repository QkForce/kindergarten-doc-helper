from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.steps.common.step_children_scores import StepChildrenScores
from gui.steps.generator.step_docx_generate import StepDocxGenerate
from gui.widgets.wizard_widget import WizardWidget
from gui.state import GeneratorState
from gui.types import Step
from gui.constants.strings import GENERATOR_OPTIONS


class GeneratorPage(WizardWidget[GeneratorState]):
    def __init__(self, on_finish: Callable):
        state = GeneratorState()
        step_factories = [
            lambda: StepFileSelect(state),
            lambda: StepChildrenScores(state),
            lambda: StepDocxGenerate(state),
        ]
        steps = []
        for index, factory in enumerate(step_factories):
            step = Step(
                title=GENERATOR_OPTIONS[index]["title"],
                description=GENERATOR_OPTIONS[index]["desc"],
                factory=factory,
            )
            steps.append(step)
        super().__init__(steps=steps, state=state, on_finish=on_finish)
