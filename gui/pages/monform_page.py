from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.widgets.wizard_widget import WizardWidget, ModuleOptions
from gui.state import ChecklistBaseState
from logic.types import Step
from gui.constants.strings import MONITORING_FORMATTER_OPTIONS
from gui.constants.icons import IconPaths


class MonFormPage(WizardWidget[ChecklistBaseState]):
    def __init__(self, on_finish: Callable):
        state = ChecklistBaseState()
        step_factories = [
            lambda: StepFileSelect(state),
        ]
        steps = []
        for index, factory in enumerate(step_factories):
            step = Step(
                title=MONITORING_FORMATTER_OPTIONS[index]["title"],
                description=MONITORING_FORMATTER_OPTIONS[index]["desc"],
                factory=factory,
            )
            steps.append(step)
        module_options = ModuleOptions(
            title="Monitoring Formatter",
            icon_path=IconPaths.FEATURE_MONFORM,
        )
        super().__init__(
            steps=steps, state=state, on_finish=on_finish, module_options=module_options
        )
