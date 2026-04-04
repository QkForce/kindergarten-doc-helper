from typing import TypeVar

from openpyxl import load_workbook
from PySide6.QtWidgets import QMessageBox
from PySide6.QtStateMachine import QStateMachine, QState
from PySide6.QtCore import Signal

from gui.steps.base_step import BaseStep
from gui.widgets.children_scores_content import ChildrenScoresWidget
from gui.widgets.status_placeholder import StatusPlaceholder, ViewState
from gui.state import ChecklistBaseState
from gui.constants.strings import AppStrings
from logic.loaders.universal_checklist_loader import UniversalChecklistLoader
from logic.worker import start_worker_task

T = TypeVar("T", bound=ChecklistBaseState)


class StepChildrenScores(BaseStep[T]):
    sig_loading = Signal()
    sig_result = Signal()
    sig_empty = Signal()
    sig_error = Signal()

    def setup_ui(self):
        self.last_error = None
        self.status_placeholder = StatusPlaceholder()
        self.content_widget = ChildrenScoresWidget()

        self.layout.addWidget(self.status_placeholder)
        self.layout.addWidget(self.content_widget)

        self.content_widget.hide()

    def setup_state_machine(self):
        self.machine = QStateMachine()

        # --- States ---
        self.state_loading = QState()
        self.state_result = QState()
        self.state_empty = QState()
        self.state_error = QState()

        # --- Loading state ---
        self.state_loading.entered.connect(
            lambda: self.status_placeholder.setState(
                ViewState.LOADING,
                AppStrings.LOADING_CHILDREN_SCORES_TITLE,
                AppStrings.LOADING_CHILDREN_SCORES_DESC,
            )
        )
        self.state_loading.assignProperty(self.status_placeholder, "visible", True)
        self.state_loading.assignProperty(self.content_widget, "visible", False)

        # --- Result state ---
        self.state_result.assignProperty(self.status_placeholder, "visible", False)
        self.state_result.assignProperty(self.content_widget, "visible", True)

        # --- No items ---
        self.state_empty.entered.connect(
            lambda: self.status_placeholder.setState(
                ViewState.EMPTY,
                AppStrings.EMPTY_CHILDREN_SCORES_TITLE,
                AppStrings.EMPTY_CHILDREN_SCORES_DESC,
            )
        )
        self.state_empty.assignProperty(self.status_placeholder, "visible", True)
        self.state_empty.assignProperty(self.content_widget, "visible", False)

        # --- Error state ---
        self.state_error.entered.connect(
            lambda: self.status_placeholder.setState(
                ViewState.ERROR,
                AppStrings.ERROR_CHILDREN_SCORES_TITLE,
                AppStrings.ERROR_CHILDREN_SCORES_DESC.format(self.last_error),
            )
        )
        self.state_error.assignProperty(self.status_placeholder, "visible", True)
        self.state_error.assignProperty(self.content_widget, "visible", False)

        # --- Transitions ---
        self.state_loading.addTransition(self.sig_result, self.state_result)
        self.state_loading.addTransition(self.sig_empty, self.state_empty)
        self.state_loading.addTransition(self.sig_error, self.state_error)

        self.state_result.addTransition(self.sig_loading, self.state_loading)
        self.state_empty.addTransition(self.sig_loading, self.state_loading)
        self.state_error.addTransition(self.sig_loading, self.state_loading)

        # Add all states
        self.machine.addState(self.state_loading)
        self.machine.addState(self.state_result)
        self.machine.addState(self.state_empty)
        self.machine.addState(self.state_error)

        # Initial
        self.machine.setInitialState(self.state_loading)
        self.machine.start()

    def connect_signals(self):
        pass

    def run_auto_load(self):
        try:
            self.sig_loading.emit()
            self.has_errors = False
            self.workbook = load_workbook(self.state.file_path, read_only=True)
            sheet = self.workbook[self.state.sheet_name]
            self.loader = UniversalChecklistLoader(sheet)
            start_worker_task(self.loader.load_auto, self._loaded, self._load_failed)
        except Exception as e:
            print(e)
            self.last_error = str(e)
            self.sig_error.emit()

    def validate_before_next(self):
        return True

    def set_state(self, result):
        start_row, end_row, name_col = result["children_data"]
        self.state.children_start_row = start_row
        self.state.children_end_row = end_row
        self.state.children_col = name_col

        metrics, code_row, desc_row, start_col, end_col = result["metrics_data"]
        self.state.metric_code_row = code_row
        self.state.metric_desc_row = desc_row
        self.state.metric_start_col = start_col
        self.state.metric_end_col = end_col
        self.state.source_metrics = metrics

        self.state.children_scores = result["children_scores"]

    def _loaded(self, result):
        if hasattr(self, "workbook"):
            self.workbook.close()
        self.set_state(result)
        self._process_result(result["children_scores"])

    def _load_failed(self, err):
        if hasattr(self, "workbook"):
            self.workbook.close()
        self.last_error = str(err)
        self.sig_error.emit()

    def _process_result(self, children_scores):
        if children_scores and len(children_scores) > 0:
            self.content_widget.set_data(children_scores, self.state.metric_codes)
            self.sig_result.emit()
        else:
            self.sig_empty.emit()
