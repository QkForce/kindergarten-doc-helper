import functools
from PySide6.QtWidgets import QMessageBox, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal
from PySide6.QtStateMachine import QStateMachine, QState

from gui.widgets.manual_load_children_widget import ManualLoadChildrenWidget
from gui.widgets.loading_plug import LoadingPlug
from gui.widgets.children_table import ChildrenTable
from gui.widgets.empty_plug import EmptyPlug
from gui.steps.step_widget import StepWidget
from logic.loaders.children_loader import ChildrenLoader
from logic.worker import start_worker_task


class StepChildrenList(StepWidget):
    sig_loading = Signal()
    sig_result = Signal()
    sig_empty = Signal()
    sig_error = Signal()

    def setup_ui(self):
        self.title = "Кезең 2 / 5: Балалар тізімін жүктеу"
        self.description = (
            "Автоматты табылған балалардың аты-жөнін тексеріңіз. "
            "Егер дұрыс болмаса, онда қолмен баптау арқылы жүктеп көріңіз."
        )

        self.loading_plug = LoadingPlug(
            "Файл талдануда... Күте тұрыңыз.",
            "Өрістерді автоматты түрде анықтау жүріп жатыр.",
        )
        self.content_widget = ChildrenTable()
        self.empty_plug = EmptyPlug(
            "Балалар табылмады",
            "• Файлда балалар тізімі бар екеніне көз жеткізіңіз<br>"
            "• Немесе қолмен баптау арқылы жүктеп көріңіз",
        )
        self.btn_toggle = QPushButton(
            "Автоматты анықтау дұрыс жұмыс істемеді ме? Өрістерді қолмен баптаңыз."
        )
        self.btn_toggle.setProperty("btn-type", "link")
        self.manual_load_widget = ManualLoadChildrenWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.loading_plug)
        layout.addWidget(self.content_widget)
        layout.addWidget(self.empty_plug)
        layout.addWidget(self.btn_toggle)
        layout.addWidget(self.manual_load_widget)

        self.loading_plug.hide()
        self.content_widget.hide()
        self.empty_plug.hide()
        self.btn_toggle.hide()
        self.manual_load_widget.hide()

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
        self.state_loading.assignProperty(self.btn_toggle, "visible", False)
        self.state_loading.assignProperty(self.manual_load_widget, "visible", False)

        # --- Result state ---
        self.state_result.assignProperty(self.loading_plug, "visible", False)
        self.state_result.assignProperty(self.content_widget, "visible", True)
        self.state_result.assignProperty(self.empty_plug, "visible", False)
        self.state_result.assignProperty(self.btn_toggle, "visible", True)
        self.state_result.assignProperty(self.manual_load_widget, "visible", False)

        # --- No items ---
        self.state_empty.assignProperty(self.loading_plug, "visible", False)
        self.state_empty.assignProperty(self.content_widget, "visible", False)
        self.state_empty.assignProperty(self.empty_plug, "visible", True)
        self.state_empty.assignProperty(self.btn_toggle, "visible", True)
        self.state_empty.assignProperty(self.manual_load_widget, "visible", True)

        # --- Error state ---
        self.state_error.assignProperty(self.loading_plug, "visible", False)
        self.state_error.assignProperty(self.content_widget, "visible", False)
        self.state_error.assignProperty(self.empty_plug, "visible", True)
        self.state_error.assignProperty(self.btn_toggle, "visible", True)
        self.state_error.assignProperty(self.manual_load_widget, "visible", True)

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
        self.btn_toggle.clicked.connect(self.on_press_btn_toggle)
        self.manual_load_widget.manual_load_clicked.connect(self.on_manual_load)

    def run_auto_load(self):
        try:
            self.sig_loading.emit()
            self.loader = ChildrenLoader(self.state.workbook[self.state.sheet_name])
            start_worker_task(self.loader.load_auto, self._loaded, self._load_failed)
        except Exception as e:
            QMessageBox.critical(self, "Қате", f"Автоматты жүктеу кезінде қате: {e}")
            self.sig_error.emit()

    def validate_before_next(self):
        return True

    def set_state(self, start_row, end_row, name_col):
        self.state.children_start_row = start_row
        self.state.children_end_row = end_row
        self.state.children_col = name_col

    def on_press_btn_toggle(self):
        self.manual_load_widget.setVisible(not self.manual_load_widget.isVisible())

    def on_manual_load(self, start_row, end_row, name_col):
        try:
            self.sig_loading.emit()
            loader_func = functools.partial(
                self.loader.load_manual, start_row, end_row, name_col
            )
            start_worker_task(loader_func, self._loaded, self._load_failed)
            self.on_press_btn_toggle()
        except Exception as e:
            QMessageBox.critical(self, "Қате", f"Қолмен жүктеу кезінде қате: {e}")
            self.sig_error.emit()

    def _loaded(self, result):
        children, start_row, end_row, name_col = result
        self.set_state(start_row, end_row, name_col)
        self._process_result(children)

    def _load_failed(self, err):
        self.sig_error.emit()
        QMessageBox.critical(self, "Қате", f"Автоматты жүктеу кезінде қате: {err}")

    def _process_result(self, children):
        if children and len(children) > 0:
            self.content_widget.set_data(children)
            self.sig_result.emit()
        else:
            self.sig_empty.emit()
