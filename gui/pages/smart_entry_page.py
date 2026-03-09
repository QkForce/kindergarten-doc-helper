from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.steps.smart_entry.step_child_assessment import StepChildAssessment
from gui.steps.common.step_file_export import StepFileExport, StepFileExportOptions
from gui.widgets.wizard_widget import WizardWidget
from gui.state import SmartEntryState
from logic.exporter import SmartEntryExporter
from gui.types import Step
from gui.constants.strings import SMART_ENTRY_OPTIONS


class SmartEntryPage(WizardWidget[SmartEntryState]):
    def __init__(self, on_finish: Callable):
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
            lambda: StepFileSelect(state),
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
        super().__init__(steps=steps, state=state, on_finish=on_finish)

    def get_progress_title(self, lbl, current, total):
        if current == 0 and total == 0:
            return "Деректерді жүктеу"
        return f"Файлға жазу процесі: {current}/{total}"

    def get_progress_desc(self, lbl, current, total):
        if current == 0 and total == 0:
            return "Деректер мониторинг файлынан қайта жүктелуде"
        return f"Бағалары файлға жазылуда: {lbl}"
