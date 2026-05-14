from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.steps.step_monform import StepMonitoringFormatter
from gui.steps.common.step_file_export import StepFileExport, StepFileExportOptions
from gui.widgets.wizard_widget import WizardWidget, ModuleOptions
from gui.state import MonFormState
from logic.exporter import MonFormExporter
from logic.types import Step
from gui.constants.strings import MONITORING_FORMATTER_OPTIONS
from gui.constants.icons import IconPaths


class MonFormPage(WizardWidget[MonFormState]):
    def __init__(self, on_finish: Callable):
        state = MonFormState()
        options = StepFileExportOptions(
            file_name="Мониторинг (2025-2026).xlsx",
            file_filter="Excel Files (*.xlsx)",
            file_extension=".xlsx",
            get_progress_title=self.get_progress_title,
            get_progress_desc=self.get_progress_desc,
            result_title="Мониторинг файлы дайын",
            result_desc="Мониторинг файлын төменгі батырма арқылы ала аласыз.",
        )
        step_factories = [
            lambda: StepFileSelect(state),
            lambda: StepMonitoringFormatter(state),
            lambda: StepFileExport(state, exporter=MonFormExporter(), options=options),
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

    def get_progress_title(self, lbl, current, total):
        if current == 0 and total == 0:
            return "Дайындық..."
        return f"Өңдеу процесі: {current}/{total}"

    def get_progress_desc(self, lbl, current, total):
        if current == 0 and total == 0:
            return "Файл оқылуда және құрылымы анықталуда..."
        return f"Қазіргі қадам: {lbl}"
