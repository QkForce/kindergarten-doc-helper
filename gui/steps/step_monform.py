from PySide6.QtWidgets import (
    QCheckBox,
    QMessageBox,
)

from gui.steps.base_step import BaseStep
from gui.state import MonFormState
from gui.constants.strings import MONFORM_CHECKBOXES, AppStrings


class StepMonitoringFormatter(BaseStep[MonFormState]):
    def setup_ui(self):
        self.checkboxes = {}
        for action in MONFORM_CHECKBOXES:
            cb = QCheckBox(action["label"])
            cb.setObjectName(action["id"])
            cb.setChecked(True)
            self.layout.addWidget(cb)
            self.checkboxes[action["id"]] = cb

        self.layout.addStretch()

    def setup_state_machine(self):
        return

    def connect_signals(self):
        return

    def run_auto_load(self):
        return

    def validate_before_next(self):
        actions = {id: cb.isChecked() for id, cb in self.checkboxes.items()}
        if not any(actions.values()):
            QMessageBox.warning(
                self, AppStrings.WARNING_TITLE, AppStrings.MONFORM_NO_ACTION_SELECTED
            )
            return False
        self.state.actions = actions
        return True
