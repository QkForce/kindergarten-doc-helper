from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.steps.smart_entry.step_child_assessment import StepChildAssessment
from gui.steps.common.step_file_export import StepFileExport, StepFileExportOptions
from gui.widgets.wizard_widget import WizardWidget
from gui.state import SmartEntryState
from logic.exporter import SmartEntryExporter


class SmartEntryPage(WizardWidget[SmartEntryState]):
    def __init__(self, on_finish: Callable):
        state = SmartEntryState()
        options = StepFileExportOptions(
            file_name="Мониторинг (2025-2026).xlsx",
            file_filter="Excel Files (*.xlsx)",
            file_extension=".xlsx",
            get_progress_desc=lambda fullname: f"Деректер өңделіп жатқан бала: {fullname}",
            result_desc="Мониторинг файлы дайын. Оны төменгі батырма арқылы ала аласыз.",
        )
        step_factories = [
            lambda: StepFileSelect(state),
            lambda: StepChildAssessment(state),
            lambda: StepFileExport(
                state, exporter=SmartEntryExporter(), options=options
            ),
        ]
        super().__init__(
            step_factories=step_factories, state=state, on_finish=on_finish
        )
