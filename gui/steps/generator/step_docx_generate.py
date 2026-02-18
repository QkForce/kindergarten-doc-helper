import functools
from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtStateMachine import QStateMachine, QState
from PySide6.QtGui import QPixmap

from gui.steps.step_widget import StepWidget
from gui.widgets.file_picker import FilePickerWidget
from logic.docx_tools import create_children_grow_cards
from logic.metrics_tools import prepare_all_children_grow_card_data
from logic.worker import start_worker_task
from logic.config_tools import get_age_group_data


class StepDocxGenerate(StepWidget):
    temp_file_path: str = ""
    docx_file = None
    sig_start_state = Signal()
    sig_progress_state = Signal()
    sig_result_state = Signal()
    sig_error_state = Signal()
    sig_progress = Signal(str, int, int)

    def setup_ui(self):
        self.title = "Кезең 5 / 5: Жеке даму картасын дайындау"
        self.description = (
            "Шаблондық файл таңдап, генерацияны орындауға жіберіңіз. "
            "Генерация сәтті аяқталғаннан кейін нәтиже жүктелуге дайын болады. \n"
            "Ескерту: генерация процесі кезінде шаблондық файлға ешқандай өзгеріс енгізілмеуі "
            "және файл басқа орынға көшірілмеуі бағдарламаның дұрыс жұмысы үшін қажет."
        )
        self.sig_progress.connect(self._listen_progress)
        layout = QVBoxLayout(self)

        self.file_select_widget = FilePickerWidget(
            "Шаблондық файл",
            "Файлды таңдау",
            "Шаблондық файлды таңдау",
            "",
            "Document Files (*.docx)",
        )
        self.btn_generate = QPushButton("Генерацияны бастау")
        self.btn_generate.setProperty("btn-size", "large")
        self.btn_generate.setProperty("btn-type", "success")

        self.progress_title = QLabel("Генерация процесі: 0/0")

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

        result_title = QLabel("Генерация сәтті аяқталды!")
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

        layout.addWidget(self.file_select_widget)
        layout.addWidget(self.btn_generate)
        layout.addWidget(self.process_progress_frame)
        layout.addWidget(self.process_result_frame)
        layout.addStretch()

        self.process_progress_frame.hide()
        self.process_result_frame.hide()

    def setup_state_machine(self):
        self.machine = QStateMachine()

        st_start = QState()
        st_progress = QState()
        st_result = QState()
        st_error = QState()

        # --- START MODE ---
        st_start.assignProperty(self.file_select_widget, "enabled", True)
        st_start.assignProperty(self.btn_generate, "visible", True)
        st_start.assignProperty(self.process_progress_frame, "visible", False)
        st_start.assignProperty(self.process_result_frame, "visible", False)

        # --- PROGRESS MODE ---
        st_progress.assignProperty(self.file_select_widget, "enabled", False)
        st_progress.assignProperty(self.btn_generate, "visible", False)
        st_progress.assignProperty(self.process_progress_frame, "visible", True)
        st_progress.assignProperty(self.process_result_frame, "visible", False)

        # --- RESULT MODE ---
        st_result.assignProperty(self.file_select_widget, "enabled", False)
        st_result.assignProperty(self.btn_generate, "visible", False)
        st_result.assignProperty(self.process_progress_frame, "visible", False)
        st_result.assignProperty(self.process_result_frame, "visible", True)

        # --- ERROR MODE ---
        st_error.assignProperty(self.file_select_widget, "enabled", True)
        st_error.assignProperty(self.btn_generate, "visible", True)
        st_error.assignProperty(self.process_progress_frame, "visible", False)
        st_error.assignProperty(self.process_result_frame, "visible", False)

        # --- TRANSITIONS ---
        st_start.addTransition(self.sig_progress_state, st_progress)
        st_progress.addTransition(self.sig_result_state, st_result)
        st_start.addTransition(self.sig_start_state, st_start)
        st_progress.addTransition(self.sig_error_state, st_error)

        # default state
        self.machine.addState(st_start)
        self.machine.addState(st_progress)
        self.machine.addState(st_result)
        self.machine.addState(st_error)

        self.machine.setInitialState(st_start)
        self.machine.start()

    def connect_signals(self):
        self.file_select_widget.fileSelected.connect(self.on_select_template)
        self.btn_generate.clicked.connect(self.on_press_generate)
        self.btn_save.clicked.connect(self.on_save)

    def run_auto_load(self):
        self.sig_start_state.emit()

    def validate_before_next(self):
        return True

    def _listen_progress(self, fullname, current_index, total_children):
        self.progress_title.setText(
            f"Генерация процесі: {current_index}/{total_children}"
        )
        self.progress_bar.setValue(current_index / total_children * 100)
        self.progress_description.setText(
            f"Даму картасы жасалған жатқан бала: {fullname}"
        )

    def on_select_template(self, file_path):
        self.temp_file_path = file_path

    def _generation_finished(self, docx_file):
        self.docx_file = docx_file
        self.sig_result_state.emit()

    def _generation_failed(self, error):
        QMessageBox.critical(self, "Қате", f"Генерация кезінде қате: {error}")
        self.sig_error_state.emit()

    def on_press_generate(self):
        if not self.temp_file_path:
            QMessageBox.warning(
                self, "Файл таңдалмады", "Алдымен шаблондық файлды таңдауыңыз керек."
            )
            return
        try:
            self.sig_progress_state.emit()
            age_group_data = get_age_group_data(self.state.age_group)
            all_children_data = prepare_all_children_grow_card_data(
                self.state.children_scores, age_group_data
            )
            worker_func = functools.partial(
                create_children_grow_cards,
                self.temp_file_path,
                all_children_data,
                self.sig_progress.emit,
            )
            start_worker_task(
                worker_func, self._generation_finished, self._generation_failed
            )
        except Exception as e:
            QMessageBox.critical(self, "Қате", f"Генерация кезінде қате: {e}")
            self.sig_error_state.emit()

    def on_save(self):
        if not self.docx_file:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Қайда сақтайсыз?",
            "Балалардың даму картасы.docx",
            "DOCX Files (*.docx)",
        )
        if not file_path:
            return

        if not file_path.lower().endswith(".docx"):
            file_path += ".docx"

        self.docx_file.save(file_path)

        QMessageBox.information(
            self, "Сақтау сәтті аяқталды", f"Құжат сақталды:\n{file_path}"
        )
