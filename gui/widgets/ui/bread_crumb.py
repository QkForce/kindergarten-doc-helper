from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QLabel, QWidget

from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.utils.icon_utils import get_svg_pixmap


class ModuleOptions:
    def __init__(self, title: str, icon_path: str):
        self.title = title
        self.icon_path = icon_path


class BreadCrumb(QWidget):
    def __init__(self, on_click_logo, module_options: ModuleOptions, parent=None):
        super().__init__(parent)

        logo_btn = QPushButton("K")
        logo_btn.setObjectName("breadcrumb_logo")
        logo_btn.setFixedSize(32, 32)
        logo_btn.clicked.connect(on_click_logo)

        chevron_pixmap = get_svg_pixmap(IconPaths.CHEVRON_RIGHT, AppColors.PRIMARY, 16)
        chevron_icon = QLabel()
        chevron_icon.setPixmap(chevron_pixmap)
        chevron_icon.setObjectName("breadcrumb_chevron_icon")

        module_pixmap = get_svg_pixmap(module_options.icon_path, AppColors.PRIMARY, 20)
        module_icon = QLabel()
        module_icon.setPixmap(module_pixmap)
        module_label = QLabel(module_options.title)

        module_label_frame = QFrame()
        module_label_frame.setFixedHeight(30)
        module_label_frame.setObjectName("breadcrumb_module_label_frame")
        module_label_layout = QHBoxLayout(module_label_frame)
        module_label_layout.setContentsMargins(5, 0, 5, 0)
        module_label_layout.addWidget(module_icon)
        module_label_layout.addWidget(module_label)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(logo_btn)
        layout.addSpacing(10)
        layout.addWidget(chevron_icon)
        layout.addSpacing(10)
        layout.addWidget(module_label_frame)
