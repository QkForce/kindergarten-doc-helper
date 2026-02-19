from typing import List, Callable, TypeVar, Generic
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

T = TypeVar("T")


class WizardWidget(QWidget, Generic[T]):
    def __init__(
        self, step_factories: List[Callable[[], QWidget]], state: T, on_finish: Callable
    ):
        super().__init__()
        self._step_factories = step_factories
        self.state = state
        self.on_finish = on_finish

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

    def _on_finish(self):
        # 1. Delete all widgets in the stack
        while self.stack.count() > 0:
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()

        # 2. Clear list
        self.steps = [None] * len(self._step_factories)

        # 3. Reset state
        if hasattr(self.state, "reset"):
            self.state.reset()

        # 4. Return to step one
        self.current_step = 0
        self.update_ui()

    def update_ui(self):
        # ensure current widget is created and show it
        widget = self.get_step(self.current_step)
        if widget:
            self.stack.setCurrentWidget(widget)

        # progress
        total = len(self._step_factories)
        self.progress_bar.setValue(int((self.current_step + 1) / total * 100))
        self.progress_title.setText(widget.title)
        self.progress_description.setText(widget.description)

        # back button
        is_first = self.current_step == 0
        self.btn_back.setEnabled(not is_first)
        self.btn_back.setProperty("btn-type", "disabled" if is_first else "neutral")
        self.btn_back.style().polish(self.btn_back)

        # next button
        is_last = self.current_step == total - 1
        try:
            self.btn_next.clicked.disconnect()
        except RuntimeError:
            pass
        if is_last:
            self.btn_next.setText("Аяқтау")
            self.btn_next.setEnabled(True)
            self.btn_next.setProperty("btn-type", "primary")
            self.btn_next.clicked.connect(self.on_finish)
            self.btn_next.clicked.connect(self._on_finish)
        else:
            self.btn_next.setText("Келесі")
            self.btn_next.setEnabled(True)
            self.btn_next.setProperty("btn-type", "primary")
            self.btn_next.clicked.connect(self.on_next)
        self.btn_next.style().polish(self.btn_next)
