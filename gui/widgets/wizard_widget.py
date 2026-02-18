from typing import List, Callable
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

from logic.app_state import AppState


class WizardWidget(QWidget):
    def __init__(self, step_factories: List[Callable[[], QWidget]], state: AppState):
        super().__init__()
        self._step_factories = step_factories
        self.state = state

        # OUTER CONTAINER
        self.outer_layout = QHBoxLayout(self)
        self.outer_layout.setObjectName("outer_container")
        self.outer_layout.setAlignment(Qt.AlignCenter)

        # CENTRAL PANEL (DESIGN KEPT)
        self.central_panel = QFrame()
        self.central_panel.setObjectName("central_panel")
        self.central_panel.setMinimumWidth(600)
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

        self.progress_description = QLabel()
        self.progress_description.setWordWrap(True)
        self.progress_description.setObjectName("progress_description")
        panel_layout.addWidget(self.progress_description)

        # STACKED WIDGET (lazy load)
        self.stack = QStackedWidget()
        panel_layout.addWidget(self.stack)

        # Step placeholders (None – not yet created)
        self.steps = [None] * len(step_factories)

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
        self.outer_layout.addStretch(10)
        self.outer_layout.addWidget(self.central_panel, 80)
        self.outer_layout.addStretch(10)

        # initial step
        self.current_step = 0
        self.update_ui()  # initial UI (this will lazy-create first step)

    # --- lazy loader ---
    def get_step(self, index: int):
        """Создаёт шаг при первом обращении и добавляет в stack."""
        if not (0 <= index < len(self.steps)):
            return None
        if self.steps[index] is None:
            widget = self._step_factories[index]()
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
        total = len(self._step_factories)
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
