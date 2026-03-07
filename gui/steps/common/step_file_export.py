from typing import TypeVar

from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtStateMachine import QStateMachine, QState
from PySide6.QtGui import QPixmap

from gui.steps.step_widget import StepWidget
from gui.state import ChecklistBaseState
from gui.constants.strings import AppStrings
from logic.worker import start_worker_task
from logic.config_tools import get_age_group_data

T = TypeVar("T", bound=ChecklistBaseState)


class StepFileExportOptions:
    def __init__(
        self,
        file_name: str = "Балалардың даму картасы.docx",
        file_filter: str = "DOCX Files (*.docx)",
        file_extension: str = ".docx",
        get_progress_desc: callable = lambda fullname: f"Даму картасы жасалып жатқан бала: {fullname}",
        result_desc: str = "Балалардың даму картасы дайын. Оны төменгі батырма арқылы ала аласыз.",
    ):
        self.file_name = file_name
        self.file_filter = file_filter
        self.file_extension = file_extension
        self.get_progress_desc = get_progress_desc
        self.result_desc = result_desc


class StepFileExport(StepWidget[T]):
    sig_progress_state = Signal()
    sig_result_state = Signal()
    sig_error_state = Signal()
    sig_progress = Signal(str, int, int)

    def __init__(self, state, exporter, options: StepFileExportOptions = None):
        super().__init__(state, parent=None)
        self.result_file = None
        self.sig_progress.connect(self._listen_progress)
        self.exporter = exporter
        self.options = options or {}

    def setup_ui(self):
        self.title = AppStrings.GENERATOR.STEP_3_TITLE
        self.description = AppStrings.GENERATOR.STEP_3_DESC
        layout = QVBoxLayout(self)

        self.progress_title = QLabel("Экспорт процесі: 0/0")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setTextVisible(False)

        self.progress_description = QLabel("Даму картасы жасалып жатқан бала: NAME")

        process_progress_layout = QVBoxLayout()
        process_progress_layout.addWidget(self.progress_title)
        process_progress_layout.addWidget(self.progress_bar)
        process_progress_layout.addWidget(self.progress_description)
        self.process_progress_frame = QFrame(self)
        self.process_progress_frame.setProperty("frame-style", "box")
        self.process_progress_frame.setLayout(process_progress_layout)

        result_status_img_label = QLabel()
        result_status_img_label.setAlignment(Qt.AlignCenter)
        result_status_img_label.setPixmap(
            QPixmap("gui\\resources\\icons\\check_circle.png")
        )

        result_title = QLabel("Экспорт сәтті аяқталды!")
        result_title.setProperty("lbl-level", "h2")

        result_description = QLabel(
            "Балалардың даму картасы дайын. Оны төменгі батырма арқылы ала аласыз."
        )
        result_description.setProperty("lbl-level", "h3-normal")

        self.btn_save = QPushButton("Нәтижені жүктеу")
        self.btn_save.setProperty("btn-size", "large")
        self.btn_save.setProperty("btn-type", "primary")

        process_result_layout = QVBoxLayout()
        process_result_layout.addWidget(result_status_img_label)
        process_result_layout.addWidget(result_title, alignment=Qt.AlignHCenter)
        process_result_layout.addWidget(result_description, alignment=Qt.AlignHCenter)
        process_result_layout.addWidget(self.btn_save, alignment=Qt.AlignHCenter)
        self.process_result_frame = QFrame(self)
        self.process_result_frame.setProperty("frame-style", "box")
        self.process_result_frame.setLayout(process_result_layout)

        layout.addWidget(self.process_progress_frame)
        layout.addWidget(self.process_result_frame)
        layout.addStretch()

        self.process_progress_frame.hide()
        self.process_result_frame.hide()

    def setup_state_machine(self):
        self.machine = QStateMachine()
        st_progress = QState()
        st_result = QState()
        st_error = QState()

        # --- PROGRESS MODE ---
        st_progress.assignProperty(self.process_progress_frame, "visible", True)
        st_progress.assignProperty(self.process_result_frame, "visible", False)

        # --- RESULT MODE ---
        st_result.assignProperty(self.process_progress_frame, "visible", False)
        st_result.assignProperty(self.process_result_frame, "visible", True)

        # --- ERROR MODE ---
        st_error.assignProperty(self.process_progress_frame, "visible", False)
        st_error.assignProperty(self.process_result_frame, "visible", False)

        # --- TRANSITIONS ---
        st_progress.addTransition(self.sig_result_state, st_result)
        st_progress.addTransition(self.sig_error_state, st_error)

        # --- DEFAULT STATE ---
        self.machine.addState(st_progress)
        self.machine.addState(st_result)
        self.machine.addState(st_error)

        self.machine.setInitialState(st_progress)
        self.machine.start()

    def connect_signals(self):
        self.btn_save.clicked.connect(self.on_save)

    def run_auto_load(self):
        try:
            self.sig_progress_state.emit()
            age_group_data = get_age_group_data(self.state.age_group)
            self.exporter.set_data(
                self.state,
                age_group_data,
                self.sig_progress.emit,
            )
            start_worker_task(
                self.exporter.export, self._export_finished, self._export_failed
            )
        except Exception as e:
            QMessageBox.critical(self, "Қате", f"Экспорт кезінде қате: {e}")
            self.sig_error_state.emit()

    def validate_before_next(self):
        if not self.result_file:
            QMessageBox.warning(self, "Ескерту", "Құжатты жасау керек.")
            return False
        return True

    def _listen_progress(self, fullname, current_index, total_children):
        self.progress_title.setText(
            f"Экспорт процесі: {current_index}/{total_children}"
        )
        self.progress_bar.setValue(current_index / total_children * 100)
        self.progress_description.setText(self.options.get_progress_desc(fullname))

    def _export_finished(self, result_file):
        self.result_file = result_file
        self.sig_result_state.emit()

    def _export_failed(self, error):
        QMessageBox.critical(self, "Қате", f"Экспорт кезінде қате: {error}")
        self.sig_error_state.emit()

    def on_save(self):
        if not self.result_file:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Қайда сақтайсыз?",
            self.options.file_name,
            self.options.file_filter,
        )
        if not file_path:
            return

        if not file_path.lower().endswith(self.options.file_extension):
            file_path += self.options.file_extension

        self.result_file.save(file_path)

        QMessageBox.information(
            self, "Сақтау сәтті аяқталды", f"Құжат сақталды:\n{file_path}"
        )
