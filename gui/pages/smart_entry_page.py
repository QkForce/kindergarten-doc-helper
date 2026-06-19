from typing import Callable

from gui.steps.common.step_monitoring_config import StepMonitoringConfig
from gui.steps.step_child_assessment import StepChildAssessment
from gui.steps.common.step_file_export import StepFileExport, StepFileExportOptions
from gui.widgets.wizard_widget import WizardWidget, ModuleOptions
from gui.state import SmartEntryState
from logic.exporter import SmartEntryExporter
from logic.types import Step
from gui.constants.strings import SMART_ENTRY_OPTIONS
from gui.constants.icons import IconPaths


class SmartEntryPage(WizardWidget[SmartEntryState]):
    def __init__(self, on_finish: Callable, parent=None):
        state = SmartEntryState()
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
            lambda: StepMonitoringConfig(state),
            lambda: StepChildAssessment(state),
            lambda: StepFileExport(
                state, exporter=SmartEntryExporter(), options=options
            ),
        ]
        steps = []
        for index, factory in enumerate(step_factories):
            step = Step(
                title=SMART_ENTRY_OPTIONS[index]["title"],
                description=SMART_ENTRY_OPTIONS[index]["desc"],
                factory=factory,
            )
            steps.append(step)
        module_options = ModuleOptions(
            title="Smart Entry",
            icon_path=IconPaths.FEATURE_ENTRY_XLSX,
        )
        super().__init__(
            steps=steps,
            state=state,
            on_finish=on_finish,
            module_options=module_options,
            parent=parent,
        )

    def get_progress_title(self, lbl, current, total):
        if current == 0 and total == 0:
            return "Деректерді жүктеу"
        return f"Файлға жазу процесі: {current}/{total}"

    def get_progress_desc(self, lbl, current, total):
        if current == 0 and total == 0:
            return "Деректер мониторинг файлынан қайта жүктелуде"
        return f"Бағалары файлға жазылуда: {lbl}"
