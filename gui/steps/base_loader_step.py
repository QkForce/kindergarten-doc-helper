from dataclasses import dataclass

from PySide6.QtWidgets import QWidget
from PySide6.QtStateMachine import QStateMachine, QState
from PySide6.QtCore import Signal

from gui.steps.base_step import BaseStep, T
from gui.widgets.status_placeholder import StatusPlaceholder, ViewState
from logic.worker import start_worker_task


@dataclass(frozen=True)
class StepLoaderOptions:
    loading_title: str = "Деректер жүктелуде"
    loading_desc: str = "Деректер жүктеліп жатыр, күте тұрыңыз!"
    empty_title: str = "Бос деректер"
    empty_desc: str = "Жүктеу нәтижесінде ешқандай дерек табылмады!"
    error_title: str = "Қате"
    error_desc: str = "Жүктеу кезінде қате пайда болды. Қайтадан көріңіз: {}"


class BaseLoaderStep(BaseStep[T]):
    sig_loading = Signal()
    sig_result = Signal()
    sig_empty = Signal()
    sig_error = Signal()

    def __init__(
        self, state: T, options: StepLoaderOptions, content_widget: QWidget, parent=None
    ):
        self.options = options
        self.content_widget = content_widget
        super().__init__(state, parent=parent)

    def setup_ui(self):
        self.last_error = None
        self.status_placeholder = StatusPlaceholder()

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
                self.options.loading_title,
                self.options.loading_desc,
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
                self.options.empty_title,
                self.options.empty_desc,
            )
        )
        self.state_empty.assignProperty(self.status_placeholder, "visible", True)
        self.state_empty.assignProperty(self.content_widget, "visible", False)

        # --- Error state ---
        self.state_error.entered.connect(
            lambda: self.status_placeholder.setState(
                ViewState.ERROR,
                self.options.error_title,
                self.options.error_desc.format(self.last_error),
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
        raise NotImplementedError()

    def load_auto(self):
        raise NotImplementedError()

    def run_auto_load(self):
        try:
            self.sig_loading.emit()
            self.has_errors = False
            start_worker_task(self.load_auto, self._loaded, self._load_failed)
        except Exception as e:
            print(e)
            self.last_error = str(e)
            self.sig_error.emit()

    def validate_before_next(self):
        raise NotImplementedError()

    def is_result_empty(self, result):
        raise NotImplementedError()

    def loaded(self, result):
        raise NotImplementedError()

    def load_failed(self, err):
        raise NotImplementedError()

    def _loaded(self, result):
        if self.is_result_empty(result):
            self.sig_empty.emit()
        else:
            self.loaded(result)
            self.sig_result.emit()

    def _load_failed(self, err):
        self.last_error = str(err)
        self.load_failed(err)
        self.sig_error.emit()
