from typing import Callable

from gui.steps.common.step_actions_select import StepActionsSelect
from gui.steps.common.step_file_select import StepFileSelectOptions, StepFileSelect
from gui.steps.common.step_file_export import StepFileExportOptions
from gui.widgets.wizard_widget import WizardWidget, ModuleOptions
from gui.state import GrowFormState
from logic.types import Step
from gui.constants.strings import GROW_CARD_FORMATTER_OPTIONS, GROWFORM_CHECKBOXES
from gui.constants.icons import IconPaths


class GrowFormPage(WizardWidget[GrowFormState]):
    def __init__(self, on_finish: Callable, parent=None):
        state = GrowFormState()
        step_file_select_options = StepFileSelectOptions(
            file_picker_label="Балалардың даму картасы файлы (.docx)",
            file_picker_caption="Балалардың даму картасы файлын таңдаңыз",
            file_picker_filter="DOCX Files (*.docx)",
            validation_error_msg="Балалардың даму картасы файлын таңдаңыз.",
            state_file_attr_name="input_file_path",
        )
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
            lambda: StepFileSelect(state, step_file_select_options),
            lambda: StepActionsSelect(state, checkboxes_data=GROWFORM_CHECKBOXES),
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
            icon_path=IconPaths.FEATURE_GROWFORM,
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
