from gui.steps.generator.step_file_select import StepFileSelect
from gui.steps.generator.step_children_scores import StepChildrenScores
from gui.steps.generator.step_docx_generate import StepDocxGenerate
from gui.widgets.wizard_widget import WizardWidget
from gui.state import GeneratorState


class GeneratorPage(WizardWidget[GeneratorState]):
    def __init__(self):
        state = GeneratorState()
        step_factories = [
            lambda: StepFileSelect(state),
            lambda: StepChildrenScores(state),
            lambda: StepDocxGenerate(state),
        ]
        super().__init__(step_factories=step_factories, state=state)
