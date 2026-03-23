from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.steps.common.step_children_scores import StepChildrenScores
from gui.steps.step_docx_template import StepDocxTemplate
from gui.steps.common.step_file_export import StepFileExport, StepFileExportOptions
from gui.widgets.wizard_widget import WizardWidget, ModuleOptions
from gui.state import GeneratorState
from gui.types import Step
from gui.constants.strings import GENERATOR_OPTIONS
from gui.constants.icons import IconPaths
from logic.exporter import DocxGenerateExporter


class GeneratorPage(WizardWidget[GeneratorState]):
    def __init__(self, on_finish: Callable):
        state = GeneratorState()
        options = StepFileExportOptions(
            file_name="Балалардың даму картасы (generated).docx",
            file_filter="DOCX Files (*.docx)",
            file_extension=".docx",
            get_progress_title=self.get_progress_title,
            get_progress_desc=self.get_progress_desc,
            result_title="Даму картасы дайын",
            result_desc="Даму картасын төменгі батырма арқылы ала аласыз.",
        )
        step_factories = [
            lambda: StepFileSelect(state),
            lambda: StepChildrenScores(state),
            lambda: StepDocxTemplate(state),
            lambda: StepFileExport(
                state, exporter=DocxGenerateExporter(), options=options
            ),
        ]
        steps = []
        for index, factory in enumerate(step_factories):
            step = Step(
                title=GENERATOR_OPTIONS[index]["title"],
                description=GENERATOR_OPTIONS[index]["desc"],
                factory=factory,
            )
            steps.append(step)
        module_options = ModuleOptions(
            title="Generator",
            icon_path=IconPaths.FEATURE_DOCX_GENERATOR,
        )
        super().__init__(
            steps=steps, state=state, on_finish=on_finish, module_options=module_options
        )

    def get_progress_title(self, lbl, current, total):
        return f"Файлға жазу процесі: {current}/{total}"

    def get_progress_desc(self, lbl, current, total):
        return f"Деректері жазылып жатқан бала: {lbl}"
