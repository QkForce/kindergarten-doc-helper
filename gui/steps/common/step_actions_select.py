from PySide6.QtWidgets import (
    QCheckBox,
    QMessageBox,
)

from gui.steps.base_step import BaseStep
from gui.state import ActionsSelectState
from gui.constants.strings import AppStrings


class StepActionsSelect(BaseStep[ActionsSelectState]):
    def __init__(self, state, checkboxes_data: dict = {}, parent=None):
        self.checkboxes_data = checkboxes_data
        super().__init__(state, parent=parent)

    def setup_ui(self):
        self.checkboxes = {}
        for action in self.checkboxes_data:
            cb = QCheckBox(action["title"])
            cb.setObjectName(action["id"])
            cb.setChecked(action["default"])
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
                self,
                AppStrings.WARNING_TITLE,
                AppStrings.ACTIONS_SELECT_NO_ACTION_SELECTED,
            )
            return False
        self.state.actions = actions
        return True
