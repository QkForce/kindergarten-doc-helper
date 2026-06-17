from typing import Callable

from gui.steps.step_docx_template import StepDocxTemplate
from gui.steps.common.step_file_export import StepFileExportOptions
from gui.widgets.wizard_widget import WizardWidget, ModuleOptions
from gui.state import MonFormState
from logic.types import Step
from gui.constants.strings import GROW_CARD_FORMATTER_OPTIONS
from gui.constants.icons import IconPaths


class GrowFormPage(WizardWidget[MonFormState]):
    def __init__(self, on_finish: Callable, parent=None):
        state = MonFormState()
        options = StepFileExportOptions(
            file_name="Балалардың даму картасы (updated).docx",
            file_filter="DOCX Files (*.docx)",
            file_extension=".docx",
            get_progress_title=self.get_progress_title,
            get_progress_desc=self.get_progress_desc,
            result_title="Даму картасы дайын",
            result_desc="Даму картасын төменгі батырма арқылы ала аласыз.",
        )
        step_factories = [
            lambda: StepDocxTemplate(state),
        ]
        steps = []
        for index, factory in enumerate(step_factories):
            step = Step(
                title=GROW_CARD_FORMATTER_OPTIONS[index]["title"],
                description=GROW_CARD_FORMATTER_OPTIONS[index]["desc"],
                factory=factory,
            )
            steps.append(step)
        module_options = ModuleOptions(
            title="Grow Card Formatter",
            icon_path=IconPaths.FEATURE_MONFORM,
        )
        super().__init__(
            steps=steps,
            state=state,
            on_finish=on_finish,
            module_options=module_options,
            parent=parent,
        )

    def get_progress_title(self, lbl, current, total):
        return f"Файлға жазу процесі: {current}/{total}"

    def get_progress_desc(self, lbl, current, total):
        return f"Деректері жазылып жатқан бала: {lbl}"
