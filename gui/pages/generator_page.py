from gui.steps.generator.step_file_select import StepFileSelect
from gui.steps.generator.step_children_scores import StepChildrenScores
from gui.steps.generator.step_docx_generate import StepDocxGenerate
from gui.widgets.wizard_widget import WizardWidget
from logic.app_state import AppState


class GeneratorPage(WizardWidget):
    def __init__(self):
        state = AppState()
        step_factories = [
            lambda: StepFileSelect(state),
            lambda: StepChildrenScores(state),
            lambda: StepDocxGenerate(state),
        ]
        super().__init__(step_factories=step_factories, state=state)
