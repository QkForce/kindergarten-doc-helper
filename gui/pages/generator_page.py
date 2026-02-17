from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QProgressBar,
    QLabel,
    QStackedWidget,
    QFrame,
)
from PySide6.QtCore import Qt

from gui.steps.step1_file_select import Step1FileSelect
from gui.steps.step2_children_list import Step2ChildrenList
from gui.steps.step3_metrics_detect import Step3MetricsDetect
from gui.steps.step4_children_scores import Step4ChildrenScores
from gui.steps.step5_docx_generate import Step5DocxGenerate
from logic.app_state import AppState


class GeneratorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.state = AppState()

        # OUTER CONTAINER
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setObjectName("outer_container")
        self.outer_layout.setAlignment(Qt.AlignCenter)

        # CENTRAL PANEL (DESIGN KEPT)
        self.central_panel = QFrame()
        self.central_panel.setObjectName("central_panel")
        self.central_panel.setFixedWidth(750)
        self.central_panel.setMinimumHeight(500)
        panel_layout = QVBoxLayout(self.central_panel)

        # PROGRESS
        self.progress_title = QLabel("Кезең 1 / 5")
        self.progress_title.setWordWrap(True)
        self.progress_title.setObjectName("progress_title")
        panel_layout.addWidget(self.progress_title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(10)
        self.progress_bar.setTextVisible(False)
        panel_layout.addWidget(self.progress_bar)

        self.progress_description = QLabel(
            "Система автоматически определила поле ФИО и нашла первые записи. Проверьте имена:"
        )
        self.progress_description.setWordWrap(True)
        self.progress_description.setObjectName("progress_description")
        panel_layout.addWidget(self.progress_description)

        # STACKED WIDGET (lazy load)
        self.stack = QStackedWidget()
        panel_layout.addWidget(self.stack)

        # Step placeholders (None – әлі құрылмаған)
        self._step_constructors = [
            lambda: Step1FileSelect(self.state),
            lambda: Step2ChildrenList(self.state),
            lambda: Step3MetricsDetect(self.state),
            lambda: Step4ChildrenScores(self.state),
            lambda: Step5DocxGenerate(self.state),
        ]
        self.steps = [None] * len(self._step_constructors)

        # NAVIGATION BUTTONS
        nav = QHBoxLayout()
        nav.setSpacing(16)
        nav.setContentsMargins(0, 0, 0, 0)

        self.btn_back = QPushButton("Артқа")
        self.btn_next = QPushButton("Келесі")

        self.btn_back.setProperty("btn-type", "neutral")
        self.btn_next.setProperty("btn-type", "primary")

        self.btn_back.setProperty("btn-size", "large")
        self.btn_next.setProperty("btn-size", "large")

        self.btn_back.setFlat(False)
        self.btn_next.setFlat(False)

        self.btn_back.clicked.connect(self.on_back)
        self.btn_next.clicked.connect(self.on_next)

        nav.addWidget(self.btn_back)
        nav.addWidget(self.btn_next)
        panel_layout.addLayout(nav)

        # finalize layout
        self.outer_layout.addWidget(self.central_panel)

        # начальный шаг
        self.current_step = 0
        self.update_ui()  # initial UI (this will lazy-create first step)

    # --- lazy loader ---
    def get_step(self, index: int):
        """Создаёт шаг при первом обращении и добавляет в stack."""
        if not (0 <= index < len(self.steps)):
            return None
        if self.steps[index] is None:
            widget = self._step_constructors[index]()
            self.steps[index] = widget
            self.stack.addWidget(widget)
        return self.steps[index]

    def on_back(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_ui()

    def on_next(self):
        current_widget = self.get_step(self.current_step)
        if current_widget is None:
            return

        if not current_widget.validate_before_next():
            return

        if self.current_step >= len(self.steps) - 1:
            return

        self.current_step += 1
        self.update_ui()

        next_widget = self.get_step(self.current_step)
        if next_widget and hasattr(next_widget, "run_auto_load"):
            next_widget.run_auto_load()

    def update_ui(self):
        # ensure current widget is created and show it
        widget = self.get_step(self.current_step)
        if widget:
            self.stack.setCurrentWidget(widget)

        # прогресс
        total = len(self._step_constructors)
        self.progress_bar.setValue(int((self.current_step + 1) / total * 100))
        self.progress_title.setText(widget.title)
        self.progress_description.setText(widget.description)

        # navigation buttons
        btn_back_enabled = self.current_step > 0
        btn_back_type = "neutral" if btn_back_enabled else "disabled"
        self.btn_back.setEnabled(btn_back_enabled)
        self.btn_back.setProperty("btn-type", btn_back_type)
        self.btn_back.style().polish(self.btn_back)

        btn_next_enabled = self.current_step < total - 1
        btn_next_type = "primary" if btn_next_enabled else "disabled"
        self.btn_next.setEnabled(btn_next_enabled)
        self.btn_next.setProperty("btn-type", btn_next_type)
        self.btn_next.style().polish(self.btn_next)
