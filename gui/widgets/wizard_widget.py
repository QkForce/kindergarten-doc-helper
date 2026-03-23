from typing import List, Callable, TypeVar, Generic

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QFrame,
)

from gui.types import Step
from gui.widgets.step_indicator import StepIndicator

T = TypeVar("T")


class WizardWidget(QFrame, Generic[T]):
    def __init__(self, steps: List[Step], state: T, on_finish: Callable):
        super().__init__()
        self._step_configs = steps
        self.state = state
        self.on_finish = on_finish
        self.setObjectName("wizard_container")

        # HEADER
        logo_btn = QPushButton("K")
        logo_btn.setObjectName("wizard_logo")
        logo_btn.setFixedSize(32, 32)
        # logo_btn.clicked.connect(self.go_home)

        self.step_indicator = StepIndicator(
            [step.title for step in steps], current_step=0
        )

        header_frame = QFrame()
        header_frame.setObjectName("wizard_header_frame")
        header_frame.setContentsMargins(0, 10, 0, 10)
        header_layout = QHBoxLayout(header_frame)
        header_layout.addWidget(logo_btn)
        header_layout.addStretch()
        header_layout.addWidget(self.step_indicator)

        # STACKED WIDGET (lazy load)
        self.stack = QStackedWidget()
        self.stack.setObjectName("central_panel")
        self.stack.setMinimumWidth(600)
        self.stack.setMinimumHeight(500)

        # Step placeholders (None – not yet created)
        self.steps = [None] * len(self._step_configs)

        # NAVIGATION BUTTONS
        self.btn_back = QPushButton("Артқа")
        self.btn_back.setMinimumWidth(200)
        self.btn_back.setProperty("btn-type", "neutral")
        self.btn_back.setProperty("btn-size", "large")
        self.btn_back.setFlat(False)
        self.btn_back.clicked.connect(self.on_back)

        self.btn_next = QPushButton("Келесі")
        self.btn_next.setMinimumWidth(200)
        self.btn_next.setProperty("btn-type", "primary")
        self.btn_next.setProperty("btn-size", "large")
        self.btn_next.setFlat(False)
        self.btn_next.clicked.connect(self.on_next)

        nav_frame = QFrame()
        nav_frame.setObjectName("wizard_nav_frame")
        nav_layout = QHBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 10, 0, 10)
        nav_layout.addWidget(self.btn_back)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_next)

        # MAIN LAYOUT
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.addWidget(header_frame)
        layout.addWidget(self.stack)
        layout.addWidget(nav_frame)

        # initial step
        self.current_step = 0
        self.update_ui()  # initial UI (this will lazy-create first step)

    # --- lazy loader ---
    def get_step(self, index: int):
        # Creates step widget on first access and adds to stack
        if not (0 <= index < len(self.steps)):
            return None
        if self.steps[index] is None:
            widget = self._step_configs[index].factory()
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
        current_widget = self.get_step(self.current_step)
        if not current_widget.validate_before_next():
            return

        self.on_finish()

        # Delete all widgets in the stack
        while self.stack.count() > 0:
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()

        # Clear list
        self.steps = [None] * len(self._step_configs)

        # Reset state
        if hasattr(self.state, "reset"):
            self.state.reset()

        # Return to step one
        self.current_step = 0
        self.update_ui()

    def update_ui(self):
        # ensure current widget is created and show it
        widget = self.get_step(self.current_step)
        if widget:
            self.stack.setCurrentWidget(widget)

        # step_config = self._step_configs[self.current_step]

        # progress
        total = len(self._step_configs)
        self.step_indicator.setCurrentStep(self.current_step)
        # self.progress_bar.setValue(int((self.current_step + 1) / total * 100))
        # self.progress_title.setText(step_config.title)
        # self.progress_description.setText(step_config.description)

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
            self.btn_next.clicked.connect(self._on_finish)
        else:
            self.btn_next.setText("Келесі")
            self.btn_next.setEnabled(True)
            self.btn_next.setProperty("btn-type", "primary")
            self.btn_next.clicked.connect(self.on_next)
        self.btn_next.style().polish(self.btn_next)
