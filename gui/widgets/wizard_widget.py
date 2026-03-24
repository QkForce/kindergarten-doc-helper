from typing import List, Callable, TypeVar, Generic

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QFrame,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.types import Step
from gui.widgets.step_indicator import StepIndicator
from gui.utils.icon_utils import get_svg_pixmap

T = TypeVar("T")


class ModuleOptions:
    def __init__(self, title: str, icon_path: str):
        self.title = title
        self.icon_path = icon_path


class WizardWidget(QFrame, Generic[T]):
    def __init__(
        self,
        steps: List[Step],
        state: T,
        on_finish: Callable,
        module_options: ModuleOptions,
    ):
        super().__init__()
        self.current_step = 0
        self._step_configs = steps
        self.state = state
        self.on_finish = on_finish
        self.setObjectName("wizard_container")

        # HEADER
        logo_btn = QPushButton("K")
        logo_btn.setObjectName("wizard_logo")
        logo_btn.setFixedSize(32, 32)
        logo_btn.clicked.connect(self.close_wizard)

        chevron_icon = QLabel("❯")
        chevron_icon.setObjectName("wizard_chevron_icon")

        module_pixmap = get_svg_pixmap(module_options.icon_path, AppColors.PRIMARY, 20)
        module_icon = QLabel()
        module_icon.setPixmap(module_pixmap)
        module_label = QLabel(module_options.title)

        module_label_frame = QFrame()
        module_label_frame.setFixedHeight(30)
        module_label_frame.setObjectName("wizard_module_label_frame")
        module_label_layout = QHBoxLayout(module_label_frame)
        module_label_layout.setContentsMargins(5, 0, 5, 0)
        module_label_layout.addWidget(module_icon)
        module_label_layout.addWidget(module_label)

        self.step_indicator = StepIndicator(
            [step.title for step in steps], current_step=0
        )

        header_frame = QFrame()
        header_frame.setObjectName("wizard_header_frame")
        header_frame.setContentsMargins(0, 10, 0, 10)
        header_layout = QHBoxLayout(header_frame)
        header_layout.addWidget(logo_btn)
        header_layout.addSpacing(10)
        header_layout.addWidget(chevron_icon)
        header_layout.addSpacing(10)
        header_layout.addWidget(module_label_frame)
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
        self.btn_back.setProperty("btn-type", "ghost")
        self.btn_back.setProperty("btn-size", "large")
        self.btn_back.setFlat(False)
        self.btn_back.clicked.connect(self.handle_back_click)

        self.btn_next = QPushButton("Келесі")
        self.btn_next.setMinimumWidth(200)
        self.btn_next.setProperty("btn-type", "primary")
        self.btn_next.setProperty("btn-size", "large")
        self.btn_next.setFlat(False)
        self.btn_next.clicked.connect(self.handle_next_click)

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
        if self.current_step >= len(self.steps) - 1:
            return

        self.current_step += 1
        self.update_ui()

        next_widget = self.get_step(self.current_step)
        if next_widget and hasattr(next_widget, "run_auto_load"):
            next_widget.run_auto_load()

    def handle_back_click(self):
        is_first = self.current_step == 0
        if is_first:
            self.close_wizard()
        else:
            self.on_back()

    def handle_next_click(self):
        current_widget = self.get_step(self.current_step)
        if current_widget is None:
            return
        if not current_widget.validate_before_next():
            return
        is_last = self.current_step == len(self._step_configs) - 1
        if is_last:
            self.close_wizard()
        else:
            self.on_next()

    def close_wizard(self):
        if hasattr(self.state, "reset"):
            self.state.reset()

        while self.stack.count() > 0:
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()

        self.steps = [None] * len(self._step_configs)
        self.current_step = 0

        self.on_finish()

    def update_ui(self):
        # ensure current widget is created and show it
        widget = self.get_step(self.current_step)
        if widget:
            self.stack.setCurrentWidget(widget)

        # progress
        total = len(self._step_configs)
        self.step_indicator.setCurrentStep(self.current_step)

        # back button
        is_first = self.current_step == 0
        left_btn_icon = IconPaths.HOUSE if is_first else IconPaths.CHEVRON_LEFT
        left_btn_icon = get_svg_pixmap(left_btn_icon, AppColors.BTN_GHOST_TEXT, 16)
        self.btn_back.setText("  Басты бет" if is_first else "  Артқа")
        self.btn_back.setIcon(QIcon(left_btn_icon))
        self.btn_back.setIconSize(QSize(16, 16))
        self.btn_back.style().polish(self.btn_back)

        # next button
        is_last = self.current_step == total - 1
        right_btn_icon = None if is_last else IconPaths.CHEVRON_RIGHT
        right_btn_icon = get_svg_pixmap(right_btn_icon, AppColors.CANVAS, 16)
        self.btn_next.setText("Аяқтау  " if is_last else "Келесі  ")
        self.btn_next.setIcon(QIcon(right_btn_icon))
        self.btn_next.setIconSize(QSize(16, 16))
        self.btn_next.setLayoutDirection(Qt.RightToLeft)
        self.btn_next.style().polish(self.btn_next)
