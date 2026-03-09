from typing import Callable

from gui.steps.common.step_file_select import StepFileSelect
from gui.steps.common.step_children_scores import StepChildrenScores
from gui.steps.step_docx_fill_setup import StepDocxFillSetup
from gui.steps.common.step_file_export import StepFileExport, StepFileExportOptions
from gui.widgets.wizard_widget import WizardWidget
from gui.state import FillerState
from gui.types import Step
from gui.constants.strings import FILLER_OPTIONS
from logic.exporter import DocxFillExporter


class FillerPage(WizardWidget[FillerState]):
    def __init__(self, on_finish: Callable):
        state = FillerState()
        options = StepFileExportOptions(
            file_name="Балалардың даму картасы (filled).docx",
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
            lambda: StepDocxFillSetup(state),
            lambda: StepFileExport(state, exporter=DocxFillExporter(), options=options),
        ]
        steps = []
        for index, factory in enumerate(step_factories):
            step = Step(
                title=FILLER_OPTIONS[index]["title"],
                description=FILLER_OPTIONS[index]["desc"],
                factory=factory,
            )
            steps.append(step)
        super().__init__(steps=steps, state=state, on_finish=on_finish)

    def get_progress_title(self, lbl, current, total):
        return f"Файлға жазу процесі: {current}/{total}"

    def get_progress_desc(self, lbl, current, total):
        return f"Деректері жазылып жатқан бала: {lbl}"
