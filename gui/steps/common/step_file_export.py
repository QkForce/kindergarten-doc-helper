from typing import TypeVar, Callable

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QProgressBar,
    QLabel,
    QFrame,
)
from PySide6.QtCore import (
    QPoint,
    Qt,
    Signal,
    QPropertyAnimation,
    QEasingCurve,
    QSequentialAnimationGroup,
    QSize,
    QVariantAnimation,
)
from PySide6.QtStateMachine import QStateMachine, QState
from PySide6.QtGui import QTransform, QMovie

from gui.steps.base_step import BaseStep
from gui.state import ChecklistBaseState
from gui.constants.strings import AppStrings
from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths, AnimationPaths
from gui.utils.icon_utils import get_svg_pixmap
from gui.utils.style_utils import apply_shadow
from logic.worker import start_worker_task
from logic.config_tools import get_age_group_data

T = TypeVar("T", bound=ChecklistBaseState)


class StepFileExportOptions:
    def __init__(
        self,
        file_name: str = "Балалардың даму картасы.docx",
        file_filter: str = "DOCX Files (*.docx)",
        file_extension: str = ".docx",
        get_progress_title: Callable[
            [str, int, int], str
        ] = lambda lbl, current, total: "Экспорт процесі жүріп жатыр...",
        get_progress_desc: Callable[
            [str, int, int], str
        ] = lambda lbl, current, total: f"Деректер өңделіп жатқан бала: {lbl}",
        result_title: str = "Балалардың даму картасы дайын",
        result_desc: str = "Құжатты төменгі батырма арқылы ала аласыз.",
        error_title: str = "Қате",
        error_desc: str = "Экспорт кезінде қате пайда болды. Қайтадан көріңіз.",
    ):
        self.file_name = file_name
        self.file_filter = file_filter
        self.file_extension = file_extension
        self.get_progress_title = get_progress_title
        self.get_progress_desc = get_progress_desc
        self.result_title = result_title
        self.result_desc = result_desc
        self.error_title = error_title
        self.error_desc = error_desc


class ExportStatusWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_anim = None
        self.setFixedSize(100, 100)

        # --- PIXMAPS ---
        self.loading_movie = QMovie(AnimationPaths.LOADING)
        self.loading_movie.setScaledSize(QSize(70, 70))
        self.success_pixmap = get_svg_pixmap(
            IconPaths.SUCCESS, AppColors.CANVAS, size=48
        )
        self.error_pixmap = get_svg_pixmap(IconPaths.ERROR, AppColors.CANVAS, size=48)

        # --- Label ---
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        # --- Setup UI ---
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignCenter)

    def applyStatus(self, status):
        self.label.clear()
        if self.current_anim:
            self.current_anim.stop()

        if status == "status-loading":
            self.label.setMovie(self.loading_movie)
            self.loading_movie.start()
        elif status == "status-success":
            self.label.setPixmap(self.success_pixmap)
            self._start_success_anim()
        elif status == "status-error":
            self.label.setPixmap(self.error_pixmap)
            self._start_error_anim()

    def _start_loading_anim(self):
        # Smooth rotation animation
        self.current_anim = QVariantAnimation(self)
        self.current_anim.setDuration(1200)  # One lap time (1.2 sec)
        self.current_anim.setStartValue(0)  # 0 degrees
        self.current_anim.setEndValue(360)  # 360 degrees
        self.current_anim.setLoopCount(-1)  # Infinite rotation

        def rotate_pixmap(angle):
            # Get the base pixmap
            original_pixmap = get_svg_pixmap(
                IconPaths.LOADING, AppColors.PRIMARY, size=48
            )
            # Create a rotation transformation
            transform = QTransform().rotate(angle)
            rotated_pixmap = original_pixmap.transformed(
                transform, Qt.SmoothTransformation
            )
            # The pixmap may change size when rotated (diagonally),
            # so we keep it in the middle of the label
            self.label.setPixmap(rotated_pixmap)

        self.current_anim.valueChanged.connect(rotate_pixmap)
        self.current_anim.start()

    def _start_success_anim(self):
        # Pulse animation
        self.current_anim = QVariantAnimation(self)
        self.current_anim.setDuration(600)  # Total pulse time
        self.current_anim.setStartValue(48)  # Initial size (size=48)
        self.current_anim.setEndValue(48)  # Finally it comes back to 48
        # In the middle (0.2nd second) the icon reaches a maximum of 72 pixels.
        self.current_anim.setKeyValueAt(0.2, 72)
        # OutElastic gives a spring effect
        self.current_anim.setEasingCurve(QEasingCurve.OutElastic)

        # We redraw the pixmap with every change.
        def update_pixmap(value):
            pix = get_svg_pixmap(IconPaths.SUCCESS, AppColors.CANVAS, size=int(value))
            self.label.setPixmap(pix)

        self.current_anim.valueChanged.connect(update_pixmap)
        self.current_anim.start()

    def _start_error_anim(self):
        orig_geo = self.label.geometry()
        self.current_anim = QSequentialAnimationGroup()
        for i in range(3):
            # Shake left
            anim1 = QPropertyAnimation(self.label, b"geometry")
            anim1.setDuration(50)
            anim1.setEndValue(orig_geo.translated(-5, 0))
            # Shake right
            anim2 = QPropertyAnimation(self.label, b"geometry")
            anim2.setDuration(50)
            anim2.setEndValue(orig_geo.translated(5, 0))
            # Add to the group
            self.current_anim.addAnimation(anim1)
            self.current_anim.addAnimation(anim2)
        # Return to original position at the end
        final_anim = QPropertyAnimation(self.label, b"geometry")
        final_anim.setDuration(50)
        final_anim.setEndValue(orig_geo)
        self.current_anim.addAnimation(final_anim)
        # Start the shake animation
        self.current_anim.start()


class StepFileExport(BaseStep[T]):
    sig_progress_state = Signal()
    sig_result_state = Signal()
    sig_error_state = Signal()
    sig_progress = Signal(str, int, int)

    def __init__(self, state, exporter, options: StepFileExportOptions = None):
        self.result_file = None
        self.exporter = exporter
        self.options = options
        self.last_error = ("", "")
        super().__init__(state, parent=None)

    def setup_ui(self):
        # --- STATE ICON ---
        self.state_icon_frame = ExportStatusWidget()
        apply_shadow(self.state_icon_frame)
        state_icon_outer_layout = QVBoxLayout()
        state_icon_outer_layout.addWidget(self.state_icon_frame)
        state_icon_outer_layout.setAlignment(self.state_icon_frame, Qt.AlignCenter)

        self.title_lbl = QLabel()
        self.title_lbl.setAlignment(Qt.AlignCenter)
        self.desc_lbl = QLabel()
        self.desc_lbl.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.setFixedWidth(300)
        self.progress_bar.setTextVisible(False)
        progress_bar_layout = QHBoxLayout()
        progress_bar_layout.addStretch()
        progress_bar_layout.addWidget(self.progress_bar)
        progress_bar_layout.addStretch()

        self.btn_save = QPushButton("Нәтижені жүктеу")
        self.btn_save.setProperty("btn-size", "large")
        self.btn_save.setProperty("btn-type", "primary")
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.addStretch()
        layout.addLayout(state_icon_outer_layout)
        layout.addSpacing(20)
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.desc_lbl)
        layout.addSpacing(30)
        layout.addLayout(progress_bar_layout)
        layout.addLayout(btn_layout)
        layout.addStretch()

        self.btn_save.hide()

    def setup_state_machine(self):
        self.machine = QStateMachine()
        st_progress = QState()
        st_result = QState()
        st_error = QState()

        # --- PROGRESS MODE ---
        st_progress.entered.connect(self.run_auto_load)
        st_progress.entered.connect(
            lambda: self.state_icon_frame.applyStatus("status-loading")
        )
        st_progress.entered.connect(lambda: self.set_frame_status("status-loading"))
        st_progress.entered.connect(
            lambda: self.title_lbl.setText(self.options.get_progress_title("", 0, 0))
        )
        st_progress.entered.connect(
            lambda: self.desc_lbl.setText(self.options.get_progress_desc("", 0, 0))
        )
        st_progress.assignProperty(self.progress_bar, "value", 0)
        st_progress.assignProperty(self.progress_bar, "visible", True)
        st_progress.assignProperty(self.btn_save, "visible", False)

        # --- RESULT MODE ---
        st_result.entered.connect(
            lambda: self.state_icon_frame.applyStatus("status-success")
        )
        st_result.entered.connect(lambda: self.set_frame_status("status-success"))
        st_result.entered.connect(
            lambda: self.title_lbl.setText(self.options.result_title)
        )
        st_result.entered.connect(
            lambda: self.desc_lbl.setText(self.options.result_desc)
        )
        st_result.assignProperty(self.progress_bar, "visible", False)
        st_result.assignProperty(self.btn_save, "visible", True)

        # --- ERROR MODE ---
        st_error.entered.connect(
            lambda: self.state_icon_frame.applyStatus("status-error")
        )
        st_error.entered.connect(lambda: self.set_frame_status("status-error"))
        st_error.entered.connect(
            lambda: self.title_lbl.setText(
                self.last_error[0] or self.options.error_title
            )
        )
        st_error.entered.connect(
            lambda: self.desc_lbl.setText(self.last_error[1] or self.options.error_desc)
        )
        st_error.assignProperty(self.progress_bar, "visible", False)
        st_error.assignProperty(self.btn_save, "visible", True)

        # --- TRANSITIONS ---
        st_progress.addTransition(self.sig_result_state, st_result)
        st_progress.addTransition(self.sig_error_state, st_error)
        st_result.addTransition(self.sig_progress_state, st_progress)
        st_error.addTransition(self.sig_progress_state, st_progress)

        # --- DEFAULT STATE ---
        self.machine.addState(st_progress)
        self.machine.addState(st_result)
        self.machine.addState(st_error)

        self.machine.setInitialState(st_progress)
        self.machine.start()

    def connect_signals(self):
        self.btn_save.clicked.connect(self.on_save)
        self.sig_progress.connect(self._listen_progress)

    def run_auto_load(self):
        try:
            self.sig_progress_state.emit()
            self.result_file = None
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
            self.last_error = ("Қате", f"Экспорт кезінде қате: {e}")
            self.sig_error_state.emit()

    def validate_before_next(self):
        if not self.result_file:
            QMessageBox.warning(self, "Ескерту", "Құжатты жасау керек.")
            return False
        return True

    def _listen_progress(self, fullname, current_index, total_children):
        self.title_lbl.setText(
            self.options.get_progress_title(fullname, current_index, total_children)
        )
        self.desc_lbl.setText(
            self.options.get_progress_desc(fullname, current_index, total_children)
        )
        if total_children > 0:
            val = int((current_index / total_children) * 100)
            self.progress_bar.setValue(val)

    def _export_finished(self, result_file):
        self.result_file = result_file
        self.sig_result_state.emit()

    def _export_failed(self, error):
        self.last_error = ("Қате", f"Экспорт кезінде қате: {error}")
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

    def set_frame_status(self, status):
        self.state_icon_frame.setProperty("frame-style", status)
        self.state_icon_frame.style().unpolish(self.state_icon_frame)
        self.state_icon_frame.style().polish(self.state_icon_frame)
