import time
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.utils.icon_utils import get_svg_pixmap
from gui.widgets.settings.age_group_item_widget import AgeGroupItemWidget
from gui.widgets.settings.domain_item_widget import DomainItemWidget
from gui.widgets.settings.subject_block import SubjectBlock
from gui.widgets.icon_button import IconButton


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
        add_age_group_btn = IconButton(IconPaths.CIRCLE_PLUS, icon_size=12)
        add_age_group_btn.setProperty("btn-type", "ghost")
        add_icon = get_svg_pixmap(IconPaths.CIRCLE_PLUS, AppColors.BTN_ICON_TEXT, 12)
        add_age_group_btn.setIcon(QIcon(add_icon))
        add_age_group_btn.setFixedSize(16, 16)
        add_age_group_btn.clicked.connect(self.on_add_age_group_clicked)
        age_group_header_layout = QHBoxLayout()
        age_group_header_layout.addWidget(age_group_title)
        age_group_header_layout.addStretch()
        age_group_header_layout.addWidget(add_age_group_btn)
        age_group_header_layout.addSpacing(8)
        self.age_group_list_widget = QListWidget()
        self.age_group_list_widget.setFixedHeight(160)
        self.age_group_list_widget.itemSelectionChanged.connect(
            self.on_age_group_selection_changed
        )
        self.age_group_list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.age_group_list_empty_label = QLabel("Жас топтары жоқ")
        self.age_group_list_empty_label.setFixedHeight(30)
        self.age_group_list_empty_label.setObjectName("empty_list_label")
        self.age_group_list_empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.age_group_list_empty_label.setVisible(False)

        domain_title = QLabel("Бағыттар")
        domain_title.setObjectName("sidebar_title")
        domain_title.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        add_domain_btn = IconButton(IconPaths.CIRCLE_PLUS, icon_size=12)
        add_domain_btn.setProperty("btn-type", "ghost")
        add_icon = get_svg_pixmap(IconPaths.CIRCLE_PLUS, AppColors.BTN_ICON_TEXT, 12)
        add_domain_btn.setIcon(QIcon(add_icon))
        add_domain_btn.setFixedSize(16, 16)
        add_domain_btn.clicked.connect(self.on_add_domain_clicked)
        domain_header_layout = QHBoxLayout()
        domain_header_layout.addWidget(domain_title)
        domain_header_layout.addStretch()
        domain_header_layout.addWidget(add_domain_btn)
        domain_header_layout.addSpacing(8)
        self.domain_list_widget = QListWidget()
        self.domain_list_widget.itemSelectionChanged.connect(
            self.on_domain_selection_changed
        )
        self.domain_list_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.domain_list_empty_label = QLabel("Бағыттар жоқ")
        self.domain_list_empty_label.setFixedHeight(30)
        self.domain_list_empty_label.setObjectName("empty_list_label")
        self.domain_list_empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.domain_list_empty_label.setVisible(False)

        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebar_frame")
        sidebar_frame.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.addLayout(age_group_header_layout)
        sidebar_layout.addWidget(self.age_group_list_widget)
        sidebar_layout.addWidget(self.age_group_list_empty_label)
        sidebar_layout.addStretch()
        sidebar_layout.addSpacing(5)
        sidebar_layout.addLayout(domain_header_layout)
        sidebar_layout.addWidget(self.domain_list_widget)
        sidebar_layout.addWidget(self.domain_list_empty_label)
        sidebar_layout.addStretch()

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

        add_subject_btn = QPushButton("  Пән қосу")
        add_subject_btn.setProperty("btn-size", "small")
        add_subject_btn.setProperty("btn-type", "primary")
        add_icon = get_svg_pixmap(IconPaths.PLUS, AppColors.CANVAS, 14)
        add_subject_btn.setIcon(QIcon(add_icon))
        add_subject_btn.setFixedHeight(26)
        add_subject_btn.clicked.connect(self.on_add_subject_clicked)

        self.body_header_frame = QFrame()
        self.body_header_frame.setObjectName("body_header_frame")
        body_header_layout = QHBoxLayout(self.body_header_frame)
        body_header_layout.setContentsMargins(10, 6, 10, 6)
        body_header_layout.setSpacing(8)
        body_header_layout.addWidget(self.breadcrumb_age_group_label)
        body_header_layout.addWidget(chevron_icon)
        body_header_layout.addWidget(self.breadcrumb_domain_label)
        body_header_layout.addStretch()
        body_header_layout.addWidget(add_subject_btn)

        self.body_list = QListWidget()
        self.body_list.setObjectName("settings_subjects_list")

        self.body_empty_label = QLabel("")
        self.body_empty_label.setObjectName("empty_list_label")
        self.body_empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_empty_label.setVisible(False)

        body_layout = QVBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(self.body_header_frame, 0)
        body_layout.addWidget(self.body_list, 1)
        body_layout.addWidget(self.body_empty_label, 1)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(sidebar_frame)
        layout.addLayout(body_layout)

        self.applySettings(self.settings)

    @property
    def current_age_group_id(self):
        row = self.age_group_list_widget.currentRow()
        if row < 0:
            return None
        item = self.age_group_list_widget.item(row)
        widget = self.age_group_list_widget.itemWidget(item)
        return widget.id if widget else None

    @property
    def current_domain_id(self):
        row = self.domain_list_widget.currentRow()
        if row < 0:
            return None
        item = self.domain_list_widget.item(row)
        widget = self.domain_list_widget.itemWidget(item)
        return widget.id if widget else None

    def on_add_age_group_clicked(self):
        new_age_group = {
            "id": f"age_group_{time.time_ns()}",
            "name": f"Жас тобы {len(self.settings['age_groups']) + 1}",
            "domains": [],
        }
        self.settings["age_groups"].append(new_age_group)
        self.applySettings(
            self.settings, selected_age_group_idx=(len(self.settings["age_groups"]) - 1)
        )

    def on_delete_age_group(self, age_group_id):
        # Remove the age group from settings
        self.settings["age_groups"] = [
            ag for ag in self.settings["age_groups"] if ag["id"] != age_group_id
        ]

        # If the list is empty new_idx should be None,
        # otherwise try to find the index of the current selected age group ID,
        # if not found default to 0
        new_idx = (
            next(
                (
                    i
                    for i, ag in enumerate(self.settings["age_groups"])
                    if ag["id"] == self.current_age_group_id
                ),
                0,
            )
            if self.settings["age_groups"]
            else None
        )

        # Apply settings with the new index
        self.applySettings(self.settings, selected_age_group_idx=new_idx)

    def on_add_domain_clicked(self):
        selected_age_group_idx = self.age_group_list_widget.currentRow()
        if selected_age_group_idx < 0:
            return
        selected_ag_domains = self.settings["age_groups"][selected_age_group_idx][
            "domains"
        ]
        new_domain = {
            "id": f"domain_{time.time_ns()}",
            "name": f"Бағыт {len(selected_ag_domains) + 1}",
            "subjects": [],
        }
        selected_ag_domains.append(new_domain)
        self.applySettings(
            self.settings,
            selected_age_group_idx=selected_age_group_idx,
            selected_domain_idx=(len(selected_ag_domains) - 1),
        )

    def on_delete_domain(self, domain_id):
        current_selected_age_group_idx = self.age_group_list_widget.currentRow()
        if current_selected_age_group_idx < 0:
            return
        selected_ag_domains = self.settings["age_groups"][
            current_selected_age_group_idx
        ]["domains"]

        # Remove the domain from settings
        selected_ag_domains = [
            domain for domain in selected_ag_domains if domain["id"] != domain_id
        ]
        self.settings["age_groups"][current_selected_age_group_idx][
            "domains"
        ] = selected_ag_domains

        # If the list is empty new_idx should be None,
        # otherwise try to find the index of the current selected domain ID,
        # if not found default to 0
        new_domain_idx = (
            next(
                (
                    i
                    for i, domain in enumerate(selected_ag_domains)
                    if domain["id"] == self.current_domain_id
                ),
                0,
            )
            if selected_ag_domains
            else None
        )

        # Apply settings with the new domain index
        self.applySettings(
            self.settings,
            selected_age_group_idx=current_selected_age_group_idx,
            selected_domain_idx=new_domain_idx,
        )

    def on_age_group_selection_changed(self):
        if not self.current_age_group_id:
            return
        selected_items = self.age_group_list_widget.selectedItems()
        for i in range(self.age_group_list_widget.count()):
            item = self.age_group_list_widget.item(i)
            widget = self.age_group_list_widget.itemWidget(item)
            if widget:
                widget.setActive(item in selected_items)
            if item in selected_items:
                self.breadcrumb_age_group_label.setText(widget.name)
                self.update_domain_list()

    def on_domain_selection_changed(self):
        if self.age_group_list_widget.currentRow() < 0:
            return
        if not self.current_age_group_id:
            return
        selected_items = self.domain_list_widget.selectedItems()
        for i in range(self.domain_list_widget.count()):
            item = self.domain_list_widget.item(i)
            widget = self.domain_list_widget.itemWidget(item)
            if widget:
                widget.setActive(item in selected_items)
            if item in selected_items:
                self.breadcrumb_domain_label.setText(widget.name)
                self.update_body_list()

    def on_add_subject_clicked(self):
        if not self.current_age_group_id or not self.current_domain_id:
            return
        selected_age_group_idx = self.age_group_list_widget.currentRow()
        selected_domain_idx = self.domain_list_widget.currentRow()
        if selected_age_group_idx < 0 or selected_domain_idx < 0:
            return
        age_group = self.settings["age_groups"][selected_age_group_idx]
        domain = age_group["domains"][selected_domain_idx]
        new_subject = {
            "id": f"subject_{time.time_ns()}",
            "name": f"Пән {len(domain['subjects']) + 1}",
            "metrics": [],
        }
        domain["subjects"].append(new_subject)

        item = QListWidgetItem(self.body_list)
        custom_widget = SubjectBlock(
            new_subject["id"], new_subject["name"], new_subject["metrics"]
        )
        item.setSizeHint(custom_widget.sizeHint())

        self.body_list.addItem(item)
        self.body_list.setItemWidget(item, custom_widget)

        custom_widget.on_delete_signal.connect(self.on_delete_subject)
        custom_widget.on_add_metric_signal.connect(self.on_add_metric)
        custom_widget.on_delete_metric_signal.connect(self.on_delete_metric)

        self.body_list.scrollToBottom()

        self.body_empty_label.setVisible(False)
        self.body_list.setVisible(True)

    def on_delete_subject(self, subject_id):
        selected_age_group_idx = self.age_group_list_widget.currentRow()
        selected_domain_idx = self.domain_list_widget.currentRow()
        if selected_age_group_idx < 0 or selected_domain_idx < 0:
            return
        age_group = self.settings["age_groups"][selected_age_group_idx]
        domain = age_group["domains"][selected_domain_idx]
        domain["subjects"] = [
            subject for subject in domain["subjects"] if subject["id"] != subject_id
        ]

        for i in range(self.body_list.count()):
            item = self.body_list.item(i)
            widget = self.body_list.itemWidget(item)
            if widget and widget.subject_id == subject_id:
                self.body_list.takeItem(i)
                break

        if self.body_list.count() == 0:
            self.body_list.setVisible(False)
            self.body_empty_label.setText("Пәндер жоқ")
            self.body_empty_label.setVisible(True)

    def on_add_metric(self, subject_id, metric_data):
        selected_age_group_idx = self.age_group_list_widget.currentRow()
        selected_domain_idx = self.domain_list_widget.currentRow()
        if selected_age_group_idx < 0 or selected_domain_idx < 0:
            return
        age_group = self.settings["age_groups"][selected_age_group_idx]
        domain = age_group["domains"][selected_domain_idx]
        subject = None
        for s in domain["subjects"]:
            if s["id"] == subject_id:
                metric_data["code"] = (
                    f"{selected_age_group_idx+1}-{domain['name'][0]}.{len(s['metrics']) + 1}"
                )
                s["metrics"].append(metric_data)
                subject = s
                break
        for i in range(self.body_list.count()):
            item = self.body_list.item(i)
            widget = self.body_list.itemWidget(item)
            if widget and widget.subject_id == subject_id:
                widget.updateTable(subject["metrics"])
                widget.updateGeometry()
                item.setSizeHint(widget.sizeHint())

    def on_delete_metric(self, subject_id, metric_id):
        selected_age_group_idx = self.age_group_list_widget.currentRow()
        selected_domain_idx = self.domain_list_widget.currentRow()
        if selected_age_group_idx < 0 or selected_domain_idx < 0:
            return
        age_group = self.settings["age_groups"][selected_age_group_idx]
        domain = age_group["domains"][selected_domain_idx]
        subject = None
        for s in domain["subjects"]:
            if s["id"] == subject_id:
                s["metrics"] = [m for m in s["metrics"] if m["id"] != metric_id]
                subject = s
                break
        for i in range(self.body_list.count()):
            item = self.body_list.item(i)
            widget = self.body_list.itemWidget(item)
            if widget and widget.subject_id == subject_id:
                widget.updateTable(subject["metrics"])
                widget.updateGeometry()
                item.setSizeHint(widget.sizeHint())

    def update_domain_list(self, selected_domain_idx=None):
        self.domain_list_widget.clear()

        selected_domain_idx = selected_domain_idx or 0

        row_age = self.age_group_list_widget.currentRow()
        if row_age < 0:
            return
        age_group = self.settings["age_groups"][row_age]
        domains = age_group["domains"]

        # Fill the domain list
        for domain in domains:
            item = QListWidgetItem(self.domain_list_widget)
            custom_widget = DomainItemWidget(domain["id"], domain["name"])
            custom_widget.setFixedWidth(180)
            item.setSizeHint(custom_widget.sizeHint())
            self.domain_list_widget.addItem(item)
            self.domain_list_widget.setItemWidget(item, custom_widget)
            custom_widget.on_delete_signal.connect(self.on_delete_domain)

        # Update visibility and selection based on the new list of domains
        if len(domains) < 1:
            self.domain_list_widget.setVisible(False)
            self.domain_list_empty_label.setVisible(True)
            self.breadcrumb_domain_label.setText("")
            self.body_header_frame.setVisible(False)
            self.body_list.setVisible(False)
            self.body_empty_label.setText("Бағыттар жоқ")
            self.body_empty_label.setVisible(True)
            self.body_list.clear()
        else:
            selected_domain_idx = min(selected_domain_idx, len(domains) - 1)
            self.domain_list_widget.setVisible(True)
            self.domain_list_empty_label.setVisible(False)
            self.breadcrumb_domain_label.setText(domains[selected_domain_idx]["name"])
            self.body_header_frame.setVisible(True)
            self.body_list.setVisible(True)
            self.body_empty_label.setVisible(False)
            self.domain_list_widget.setCurrentRow(selected_domain_idx)

        self.update_body_list()

    def update_body_list(self):
        self.body_list.clear()

        row_age = self.age_group_list_widget.currentRow()
        row_domain = self.domain_list_widget.currentRow()

        if row_age < 0 or row_domain < 0:
            return

        if not self.settings["age_groups"] or row_age >= len(
            self.settings["age_groups"]
        ):
            return

        age_group = self.settings["age_groups"][row_age]

        if not age_group.get("domains") or row_domain >= len(age_group["domains"]):
            return

        domain = age_group["domains"][row_domain]

        for subject in domain.get("subjects", []):
            item = QListWidgetItem(self.body_list)
            custom_widget = SubjectBlock(
                subject["id"], subject["name"], subject["metrics"]
            )
            item.setSizeHint(custom_widget.sizeHint())
            self.body_list.addItem(item)
            self.body_list.setItemWidget(item, custom_widget)
            custom_widget.on_delete_signal.connect(self.on_delete_subject)
            custom_widget.on_add_metric_signal.connect(self.on_add_metric)
            custom_widget.on_delete_metric_signal.connect(self.on_delete_metric)

        if len(domain.get("subjects", [])) < 1:
            self.body_list.setVisible(False)
            self.body_empty_label.setText("Пәндер жоқ")
            self.body_empty_label.setVisible(True)
        else:
            self.body_list.setVisible(True)
            self.body_empty_label.setVisible(False)

    def applySettings(
        self, settings, selected_age_group_idx=None, selected_domain_idx=None
    ):
        self.age_group_list_widget.blockSignals(True)
        selected_age_group_idx = (
            selected_age_group_idx if selected_age_group_idx is not None else 0
        )
        selected_domain_idx = (
            selected_domain_idx if selected_domain_idx is not None else 0
        )
        self.age_group_list_widget.clear()
        for age_group in settings["age_groups"]:
            item = QListWidgetItem(self.age_group_list_widget)
            custom_widget = AgeGroupItemWidget(age_group["id"], age_group["name"])
            custom_widget.setFixedWidth(180)
            item.setSizeHint(custom_widget.sizeHint())
            self.age_group_list_widget.addItem(item)
            self.age_group_list_widget.setItemWidget(item, custom_widget)
            custom_widget.on_delete_signal.connect(self.on_delete_age_group)
        if len(settings["age_groups"]) < 1:
            self.age_group_list_widget.setVisible(False)
            self.age_group_list_empty_label.setVisible(True)
            self.domain_list_widget.setVisible(False)
            self.domain_list_empty_label.setText("Жас топтары жоқ")
            self.domain_list_empty_label.setVisible(True)
            self.body_header_frame.setVisible(False)
            self.body_list.setVisible(False)
            self.body_empty_label.setText("Жас топтары жоқ")
            self.body_empty_label.setVisible(True)
            self.breadcrumb_age_group_label.setText("")
            self.breadcrumb_domain_label.setText("")
            self.domain_list_widget.clear()
            self.body_list.clear()
            return
        selected_age_group_idx = min(
            selected_age_group_idx, len(settings["age_groups"]) - 1
        )
        self.age_group_list_widget.setVisible(True)
        self.age_group_list_empty_label.setVisible(False)
        self.body_header_frame.setVisible(True)
        self.body_list.setVisible(True)
        self.body_empty_label.setVisible(False)
        self.breadcrumb_age_group_label.setText(
            settings["age_groups"][selected_age_group_idx]["name"]
        )
        self.age_group_list_widget.blockSignals(False)
        self.age_group_list_widget.setCurrentRow(selected_age_group_idx)

        self.update_domain_list(selected_domain_idx=selected_domain_idx)

    def get_data(self):
        return {
            "age_groups": self.settings["age_groups"],
        }
