from enum import Enum

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

from gui.utils.icon_utils import get_svg_pixmap
from gui.constants.icons import IconPaths
from gui.constants.colors import AppColors
from gui.widgets.spinner import Spinner


class ViewState(Enum):
    LOADING = "loading"
    SUCCESS = "success"
    EMPTY = "empty"
    ERROR = "error"


class StatusPlaceholder(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        # 1. Иконка немесе Спиннер фреймі
        self.icon_frame = QFrame()
        self.icon_frame.setFixedSize(100, 100)
        self.icon_layout = QVBoxLayout(self.icon_frame)
        self.icon_layout.setAlignment(Qt.AlignCenter)

        # Иконка үшін QLabel
        self.icon_lbl = QLabel()

        # LOADING үшін Спиннер (бастапқыда жасырын)
        self.spinner = Spinner(color=AppColors.PRIMARY, size=40)
        self.spinner.setFixedSize(60, 60)

        self.icon_layout.addWidget(self.icon_lbl, alignment=Qt.AlignCenter)
        self.icon_layout.addWidget(self.spinner, alignment=Qt.AlignCenter)

        # 2. Мәтіндер
        self.title_lbl = QLabel()
        self.title_lbl.setProperty("lbl-level", "h2")
        self.title_lbl.setAlignment(Qt.AlignCenter)

        self.desc_lbl = QLabel()
        self.desc_lbl.setProperty("lbl-level", "h3-normal")
        self.desc_lbl.setWordWrap(True)
        self.desc_lbl.setAlignment(Qt.AlignCenter)
        self.desc_lbl.setFixedWidth(300)

        # Негізгі Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        layout.addStretch()
        layout.addWidget(self.icon_frame, alignment=Qt.AlignCenter)
        layout.addWidget(self.title_lbl, alignment=Qt.AlignCenter)
        layout.addWidget(self.desc_lbl, alignment=Qt.AlignCenter)
        layout.addStretch()

    def setState(self, state: ViewState, title: str = "", description: str = ""):
        self.title_lbl.setText(title)
        self.desc_lbl.setText(description)

        # 1. Спиннерді басқару
        if state == ViewState.LOADING:
            self.icon_lbl.hide()
            self.spinner.start_animation()
        else:
            self.spinner.stop_animation()
            self.icon_lbl.show()

        # 2. Конфигурация (LOADING енді status-loading қолданады)
        configs = {
            ViewState.LOADING: (None, None, "status-loading"),
            ViewState.SUCCESS: (IconPaths.SUCCESS, AppColors.SUCCESS, "status-success"),
            ViewState.EMPTY: (IconPaths.EMPTY, AppColors.WARNING, "status-empty"),
            ViewState.ERROR: (IconPaths.ERROR, AppColors.ERROR, "status-error"),
        }

        icon_path, color, frame_style = configs.get(state)

        # 3. Иконканы орнату
        if icon_path:
            pixmap = get_svg_pixmap(icon_path, color=AppColors.CANVAS, size=48)
            self.icon_lbl.setPixmap(pixmap)

        # 4. Стильді қолдану
        self.icon_frame.setProperty("frame-style", frame_style)
        self.icon_frame.style().unpolish(self.icon_frame)
        self.icon_frame.style().polish(self.icon_frame)
