from typing import Callable

from gui.constants.strings import GENERATOR_OPTIONS
from gui.constants.icons import IconPaths
from gui.steps.common.step_monitoring_config import StepMonitoringConfig
from gui.steps.common.step_children_scores import StepChildrenScores
from gui.steps.common.step_file_select import StepFileSelect, StepFileSelectOptions
from gui.steps.common.step_file_export import StepFileExport, StepFileExportOptions
from gui.widgets.wizard_widget import WizardWidget, ModuleOptions
from gui.state import GeneratorState
from logic.exporter import DocxGenerateExporter
from logic.types import Step


class GeneratorPage(WizardWidget[GeneratorState]):
    def __init__(self, on_finish: Callable, parent=None):
        state = GeneratorState()
        file_select_options = StepFileSelectOptions(
            file_picker_label="Шаблондық файл",
            file_picker_caption="Шаблондық файлды таңдау",
            file_picker_filter="Document files (*.docx)",
            validation_error_msg="Шаблондық файлды таңдаңыз!",
            state_file_attr_name="temp_file_path",
        )
        file_export_options = StepFileExportOptions(
            file_name="Балалардың даму картасы (generated).docx",
            file_filter="DOCX Files (*.docx)",
            file_extension=".docx",
            get_progress_title=self.get_progress_title,
            get_progress_desc=self.get_progress_desc,
            result_title="Даму картасы дайын",
            result_desc="Даму картасын төменгі батырма арқылы ала аласыз.",
        )
        exporter = DocxGenerateExporter()
        step_factories = [
            lambda: StepMonitoringConfig(state),
            lambda: StepChildrenScores(state),
            lambda: StepFileSelect(state, file_select_options),
            lambda: StepFileExport(state, exporter, file_export_options),
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
