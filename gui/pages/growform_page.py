from typing import Callable

from gui.constants.strings import GROW_CARD_FORMATTER_OPTIONS
from gui.constants.icons import IconPaths
from gui.state import GrowFormState
from gui.steps.step_growform_config import StepGrowFormConfig
from gui.steps.common.step_file_export import StepFileExportOptions, StepFileExport
from gui.widgets.wizard_widget import WizardWidget, ModuleOptions
from logic.types import Step
from logic.exporter import GrowFormExporter


class GrowFormPage(WizardWidget[GrowFormState]):
    def __init__(self, on_finish: Callable, parent=None):
        state = GrowFormState()
        options = StepFileExportOptions(
            file_name="Балалардың даму картасы (formated).docx",
            file_filter="DOCX Files (*.docx)",
            file_extension=".docx",
            get_progress_title=self.get_progress_title,
            get_progress_desc=self.get_progress_desc,
            result_title="Даму картасы дайын",
            result_desc="Даму картасын төменгі батырма арқылы ала аласыз.",
        )
        step_factories = [
            lambda: StepGrowFormConfig(state, parent=self),
            lambda: StepFileExport(state, GrowFormExporter(), options, parent=self),
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
        return "Файлды экспорттау"

    def get_progress_desc(self, lbl, current, total):
        return f"{current}/{total}: {lbl}"
