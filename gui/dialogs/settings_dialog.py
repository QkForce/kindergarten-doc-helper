from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt

from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.utils.icon_utils import get_svg_pixmap
from gui.widgets.settings.age_group_item_widget import AgeGroupItemWidget
from gui.widgets.settings.domain_item_widget import DomainItemWidget
from gui.widgets.settings.subject_block import SubjectBlock


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Баптаулар")
        self.setMinimumSize(950, 650)
        self.settings = settings

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
        self.body_list.setObjectName("settings_subjects_list")

        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(body_header_frame, 0)
        body_layout.addWidget(self.body_list, 1)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(sidebar_frame)
        layout.addLayout(body_layout)

        self.applySettings(self.settings)

    def on_age_group_selection_changed(self):
        selected_items = self.age_group_list_widget.selectedItems()
        for i in range(self.age_group_list_widget.count()):
            item = self.age_group_list_widget.item(i)
            widget = self.age_group_list_widget.itemWidget(item)
            if widget:
                widget.setActive(item in selected_items)
            if item in selected_items:
                self.selected_age_group_id = widget.id
                self.breadcrumb_age_group_label.setText(widget.name)
                self.update_domain_list()

    def on_domain_selection_changed(self):
        selected_items = self.domain_list_widget.selectedItems()
        for i in range(self.domain_list_widget.count()):
            item = self.domain_list_widget.item(i)
            widget = self.domain_list_widget.itemWidget(item)
            if widget:
                widget.setActive(item in selected_items)
            if item in selected_items:
                self.selected_domain_id = widget.id
                self.breadcrumb_domain_label.setText(widget.name)
                self.update_body_list()

    def update_domain_list(self):
        found_age_groups = [
            ag
            for ag in self.settings["age_groups"]
            if ag["id"] == self.selected_age_group_id
        ]
        if len(found_age_groups) < 1:
            return
        self.domain_list_widget.clear()
        age_group = found_age_groups[0]
        domains = age_group["domains"]
        for domain in domains:
            item = QListWidgetItem(self.domain_list_widget)
            custom_widget = DomainItemWidget(domain["id"], domain["name"])
            custom_widget.setFixedWidth(180)
            item.setSizeHint(custom_widget.sizeHint())
            self.domain_list_widget.addItem(item)
            self.domain_list_widget.setItemWidget(item, custom_widget)
        self.selected_domain_id = domains[0]["id"]
        self.breadcrumb_domain_label.setText(domains[0]["name"])
        item = self.domain_list_widget.item(0)
        self.domain_list_widget.setCurrentItem(item)

    def update_body_list(self):
        found_age_groups = [
            ag
            for ag in self.settings["age_groups"]
            if ag["id"] == self.selected_age_group_id
        ]
        if len(found_age_groups) < 1:
            return
        age_group = found_age_groups[0]
        found_domains = [
            domain
            for domain in age_group["domains"]
            if domain["id"] == self.selected_domain_id
        ]
        if len(found_domains) < 1:
            return
        domain = found_domains[0]
        self.body_list.clear()
        subjects = domain["subjects"]
        for subject in subjects:
            item = QListWidgetItem(self.body_list)
            custom_widget = SubjectBlock(
                subject["id"], subject["name"], subject["metrics"]
            )
            item.setSizeHint(custom_widget.sizeHint())
            self.body_list.addItem(item)
            self.body_list.setItemWidget(item, custom_widget)

    def applySettings(self, settings):
        self.age_group_list_widget.clear()
        for age_group in settings["age_groups"]:
            item = QListWidgetItem(self.age_group_list_widget)
            custom_widget = AgeGroupItemWidget(age_group["id"], age_group["name"])
            custom_widget.setFixedWidth(180)
            item.setSizeHint(custom_widget.sizeHint())
            self.age_group_list_widget.addItem(item)
            self.age_group_list_widget.setItemWidget(item, custom_widget)
        self.selected_age_group_id = settings["age_groups"][0]["id"]
        self.breadcrumb_age_group_label.setText(settings["age_groups"][0]["name"])
        item = self.age_group_list_widget.item(0)
        self.age_group_list_widget.setCurrentItem(item)

        self.update_domain_list()

    def get_data(self):
        return {
            "age_groups": self.settings["age_groups"],
        }
