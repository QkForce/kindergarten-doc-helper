from gui.steps.step1_file_select import Step1FileSelect
from gui.steps.step2_children_list import Step2ChildrenList
from gui.steps.step3_metrics_detect import Step3MetricsDetect
from gui.steps.step4_children_scores import Step4ChildrenScores
from gui.steps.step5_docx_generate import Step5DocxGenerate
from gui.widgets.wizard_widget import WizardWidget
from logic.app_state import AppState


class GeneratorPage(WizardWidget):
    def __init__(self):
        state = AppState()
        step_factories = [
            lambda: Step1FileSelect(state),
            lambda: Step2ChildrenList(state),
            lambda: Step3MetricsDetect(state),
            lambda: Step4ChildrenScores(state),
            lambda: Step5DocxGenerate(state),
        ]
        super().__init__(step_factories=step_factories, state=state)
