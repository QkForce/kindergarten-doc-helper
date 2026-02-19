from PySide6.QtWidgets import QVBoxLayout, QMessageBox
from PySide6.QtStateMachine import QStateMachine, QState
from PySide6.QtCore import Signal

from gui.steps.step_widget import StepWidget
from gui.widgets.children_scores_content import ChildrenScoresWidget
from gui.widgets.loading_plug import LoadingPlug
from gui.widgets.empty_plug import EmptyPlug
from gui.state import GeneratorState
from gui.constants.strings import AppStrings
from logic.loaders.universal_checklist_loader import UniversalChecklistLoader
from logic.worker import start_worker_task
from logic.config_tools import get_all_metric_codes


class StepChildrenScores(StepWidget[GeneratorState]):
    sig_loading = Signal()
    sig_result = Signal()
    sig_empty = Signal()
    sig_error = Signal()

    def setup_ui(self):
        self.title = AppStrings.GENERATOR.STEP_2_TITLE
        self.description = AppStrings.GENERATOR.STEP_2_DESC
        self.loading_plug = LoadingPlug(
            "Балалардың бағалары жүктелуде... Күте тұрыңыз.",
            "Файлдағы балалардың бағалары оқылуда.",
        )
        self.content_widget = ChildrenScoresWidget()
        self.empty_plug = EmptyPlug(
            "Балалардың бағалары табылмады",
            "• Файлда балалардың бағалары бар екеніне көз жеткізіңіз<br>"
            "• Немесе файлдағы деректердің дұрыстығына көз жеткізіңіз",
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.loading_plug)
        layout.addWidget(self.content_widget)
        layout.addWidget(self.empty_plug)

        self.loading_plug.hide()
        self.content_widget.hide()
        self.empty_plug.hide()

    def setup_state_machine(self):
        self.machine = QStateMachine()

        # --- States ---
        self.state_loading = QState()
        self.state_result = QState()
        self.state_empty = QState()
        self.state_error = QState()

        # --- Loading state ---
        self.state_loading.assignProperty(self.loading_plug, "visible", True)
        self.state_loading.assignProperty(self.content_widget, "visible", False)
        self.state_loading.assignProperty(self.empty_plug, "visible", False)

        # --- Result state ---
        self.state_result.assignProperty(self.loading_plug, "visible", False)
        self.state_result.assignProperty(self.content_widget, "visible", True)
        self.state_result.assignProperty(self.empty_plug, "visible", False)

        # --- No items ---
        self.state_empty.assignProperty(self.loading_plug, "visible", False)
        self.state_empty.assignProperty(self.content_widget, "visible", False)
        self.state_empty.assignProperty(self.empty_plug, "visible", True)

        # --- Error state ---
        self.state_error.assignProperty(self.loading_plug, "visible", False)
        self.state_error.assignProperty(self.content_widget, "visible", False)
        self.state_error.assignProperty(self.empty_plug, "visible", True)

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
            self.has_errors = False
            self.loader = UniversalChecklistLoader(
                self.state.workbook[self.state.sheet_name]
            )
            start_worker_task(self.loader.load_auto, self._loaded, self._load_failed)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Қате", f"Автоматты жүктеу кезінде қате: {e}")
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
        self.set_state(result)
        self._process_result(result["children_scores"])

    def _load_failed(self, err):
        self.sig_error.emit()
        QMessageBox.critical(self, "Қате", f"Автоматты жүктеу кезінде қате: {err}")

    def _process_result(self, children_scores):
        if children_scores and len(children_scores) > 0:
            metric_codes = get_all_metric_codes(self.state.age_group)
            self.content_widget.set_data(children_scores, metric_codes)
            self.sig_result.emit()
        else:
            self.sig_empty.emit()
