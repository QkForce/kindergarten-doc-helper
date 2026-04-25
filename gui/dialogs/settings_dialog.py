from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)
from PySide6.QtCore import QSize, Qt

from config.config import METRICS_SCHEMA
from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.constants.strings import AGE_GROUPS, DOMAIN_NAMES
from gui.utils.icon_utils import get_svg_pixmap
from gui.widgets.settings.age_group_item_widget import AgeGroupItemWidget
from gui.widgets.settings.domain_item_widget import DomainItemWidget
from gui.widgets.settings.subject_block import SubjectBlock


class SettingsDialog(QDialog):
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Баптаулар")
        self.setMinimumSize(950, 650)

        # SIDEBAR
        age_group_title = QLabel("Жас топтары")
        age_group_title.setObjectName("sidebar_title")
        age_group_title.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.age_group_list_widget = QListWidget()
        self.age_group_list_widget.setFixedHeight(160)
        self.age_group_list_widget.itemSelectionChanged.connect(
            self.on_age_group_selection_changed
        )
        self.age_group_list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        domain_title = QLabel("Бағыттар")
        domain_title.setObjectName("sidebar_title")
        domain_title.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.domain_list_widget = QListWidget()
        self.domain_list_widget.itemSelectionChanged.connect(
            self.on_domain_selection_changed
        )
        self.domain_list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebar_frame")
        sidebar_frame.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.addWidget(age_group_title)
        sidebar_layout.addWidget(self.age_group_list_widget)
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(domain_title)
        sidebar_layout.addWidget(self.domain_list_widget)

        # BODY
        self.breadcrumb_age_group_label = QLabel()
        self.breadcrumb_age_group_label.setObjectName("breadcrumb_label")
        self.breadcrumb_age_group_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        chevron_pixmap = get_svg_pixmap(IconPaths.CHEVRON_RIGHT, AppColors.PRIMARY, 14)
        chevron_icon = QLabel()
        chevron_icon.setPixmap(chevron_pixmap)
        chevron_icon.setObjectName("breadcrumb_chevron_icon")
        self.breadcrumb_domain_label = QLabel()
        self.breadcrumb_domain_label.setObjectName("breadcrumb_label")
        self.breadcrumb_domain_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        body_header_frame = QFrame()
        body_header_frame.setObjectName("body_header_frame")
        body_header_frame.setFixedHeight(40)
        body_header_layout = QHBoxLayout(body_header_frame)
        body_header_layout.addWidget(self.breadcrumb_age_group_label)
        body_header_layout.addWidget(chevron_icon)
        body_header_layout.addWidget(self.breadcrumb_domain_label)
        body_header_layout.addStretch()

        self.body_list = QListWidget()

        body_frame = QFrame()
        body_frame.setObjectName("body_frame")
        body_layout = QVBoxLayout(body_frame)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.addWidget(body_header_frame, 0)
        body_layout.addWidget(self.body_list, 1)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(sidebar_frame)
        layout.addWidget(body_frame)

        self.applySettings(current_settings)

    def on_age_group_selection_changed(self):
        selected_items = self.age_group_list_widget.selectedItems()
        for i in range(self.age_group_list_widget.count()):
            item = self.age_group_list_widget.item(i)
            widget = self.age_group_list_widget.itemWidget(item)
            if widget:
                widget.setActive(item in selected_items)
            if item in selected_items:
                age_group_key = widget.age_group_key
                self.selected_age_group = age_group_key
                self.breadcrumb_age_group_label.setText(AGE_GROUPS[age_group_key])
                self.update_domain_list()

    def on_domain_selection_changed(self):
        selected_items = self.domain_list_widget.selectedItems()
        for i in range(self.domain_list_widget.count()):
            item = self.domain_list_widget.item(i)
            widget = self.domain_list_widget.itemWidget(item)
            if widget:
                widget.setActive(item in selected_items)
            if item in selected_items:
                domain_key = widget.domain_key
                self.selected_domain = domain_key
                self.breadcrumb_domain_label.setText(DOMAIN_NAMES[domain_key])
                self.update_body_list()

    def update_domain_list(self):
        self.domain_list_widget.clear()
        for domain in METRICS_SCHEMA[self.selected_age_group].keys():
            item = QListWidgetItem(self.domain_list_widget)
            custom_widget = DomainItemWidget(domain)
            custom_widget.setFixedWidth(180)
            item.setSizeHint(custom_widget.sizeHint())
            self.domain_list_widget.addItem(item)
            self.domain_list_widget.setItemWidget(item, custom_widget)
        self.selected_domain = next(
            iter(METRICS_SCHEMA[self.selected_age_group].keys())
        )
        self.breadcrumb_domain_label.setText(DOMAIN_NAMES[self.selected_domain])
        item = self.domain_list_widget.item(0)
        self.domain_list_widget.setCurrentItem(item)

    def update_body_list(self):
        self.body_list.clear()
        subjects = METRICS_SCHEMA[self.selected_age_group][self.selected_domain]
        for sn, metrics in subjects.items():
            item = QListWidgetItem(self.body_list)
            custom_widget = SubjectBlock(sn, metrics)
            item.setSizeHint(custom_widget.sizeHint())
            self.body_list.addItem(item)
            self.body_list.setItemWidget(item, custom_widget)

    def applySettings(self, settings):
        self.age_group_list_widget.clear()
        for age_group in METRICS_SCHEMA.keys():
            item = QListWidgetItem(self.age_group_list_widget)
            custom_widget = AgeGroupItemWidget(age_group)
            custom_widget.setFixedWidth(180)
            item.setSizeHint(custom_widget.sizeHint())
            self.age_group_list_widget.addItem(item)
            self.age_group_list_widget.setItemWidget(item, custom_widget)
        self.selected_age_group = next(iter(METRICS_SCHEMA.keys()))
        self.breadcrumb_age_group_label.setText(AGE_GROUPS[self.selected_age_group])
        item = self.age_group_list_widget.item(0)
        self.age_group_list_widget.setCurrentItem(item)

        self.update_domain_list()

    def get_data(self):
        return {"export_path": self.path_input.text()}
