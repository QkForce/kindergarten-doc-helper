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
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.utils.icon_utils import get_svg_pixmap
from gui.widgets.settings.simple_list_widget import SimpleListWidget
from gui.widgets.settings.subject_block import SubjectBlock


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Баптаулар")
        self.setMinimumSize(950, 650)
        self.settings = settings

        # SIDEBAR
        self.age_group_list = SimpleListWidget("Жас топтары")
        self.age_group_list.on_add_signal.connect(self.on_add_age_group_clicked)
        self.age_group_list.on_selection_changed_signal.connect(
            self.on_age_group_selection_changed
        )

        self.domain_list = SimpleListWidget("Бағыттар")
        self.domain_list.on_add_signal.connect(self.on_add_domain_clicked)
        self.domain_list.on_selection_changed_signal.connect(
            self.on_domain_selection_changed
        )

        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebar_frame")
        sidebar_frame.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.addWidget(self.age_group_list)
        sidebar_layout.addSpacing(5)
        sidebar_layout.addWidget(self.domain_list)

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

    def on_add_age_group_clicked(self):
        new_age_group = {
            "id": f"age_group_{time.time_ns()}",
            "name": f"Жас тобы {len(self.settings['age_groups']) + 1}",
            "domains": [],
        }
        self.settings["age_groups"].append(new_age_group)
        self.age_group_list.addItem(
            new_age_group["id"],
            new_age_group["name"],
            "age_group_item_widget",
            self.on_edit_age_group,
            self.on_delete_age_group,
        )
        self.applySettings(
            self.settings, selected_age_group_idx=(len(self.settings["age_groups"]) - 1)
        )

    def on_edit_age_group(self, age_group_id, new_name):
        for age_group in self.settings["age_groups"]:
            if age_group["id"] == age_group_id:
                age_group["name"] = new_name
                break
        if self.age_group_list.current_id == age_group_id:
            self.breadcrumb_age_group_label.setText(new_name)

    def on_delete_age_group(self, age_group_id):
        self.settings["age_groups"] = [
            ag for ag in self.settings["age_groups"] if ag["id"] != age_group_id
        ]
        self.age_group_list.deleteItem(age_group_id)
        if self.age_group_list.list.count() > 0:
            new_idx = (
                next(
                    (
                        i
                        for i, ag in enumerate(self.settings["age_groups"])
                        if ag["id"] == self.age_group_list.current_id
                    ),
                    0,
                )
                if self.settings["age_groups"]
                else None
            )
            self.age_group_list.setCurrentRow(new_idx)
        else:
            self.age_group_list.setEmpty("Жас топтары жоқ")
            self.domain_list.clear()
            self.domain_list.setEmpty("Жас топтары жоқ")

            self.breadcrumb_age_group_label.setText("")
            self.breadcrumb_domain_label.setText("")

            self.body_header_frame.setVisible(False)
            self.body_list.clear()
            self.body_list.setVisible(False)

            self.body_empty_label.setText("Жас топтары жоқ")
            self.body_empty_label.setVisible(True)

    def on_add_domain_clicked(self):
        selected_age_group_idx = self.age_group_list.currentRow()
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
        self.domain_list.addItem(
            new_domain["id"],
            new_domain["name"],
            "domain_item_widget",
            self.on_edit_domain,
            self.on_delete_domain,
        )
        self.domain_list.setCurrentRow(len(selected_ag_domains) - 1)
        self.body_header_frame.setVisible(True)
        self.body_list.setVisible(True)
        self.body_empty_label.setVisible(self.body_list.count() == 0)

    def on_edit_domain(self, domain_id, new_name):
        selected_age_group_idx = self.age_group_list.currentRow()
        if selected_age_group_idx < 0:
            return
        selected_ag_domains = self.settings["age_groups"][selected_age_group_idx][
            "domains"
        ]
        for domain in selected_ag_domains:
            if domain["id"] == domain_id:
                domain["name"] = new_name
                break
        if self.domain_list.current_id == domain_id:
            self.breadcrumb_domain_label.setText(new_name)

    def on_delete_domain(self, domain_id):
        row_age = self.age_group_list.currentRow()
        if row_age < 0:
            return
        age_group = self.settings["age_groups"][row_age]
        age_group["domains"] = [d for d in age_group["domains"] if d["id"] != domain_id]
        self.domain_list.deleteItem(domain_id)
        if self.domain_list.list.count() > 0:
            new_idx = (
                next(
                    (
                        i
                        for i, domain in enumerate(age_group["domains"])
                        if domain["id"] == self.domain_list.current_id
                    ),
                    0,
                )
                if age_group["domains"]
                else None
            )
            self.domain_list.setCurrentRow(new_idx)
        else:
            self.update_domain_list()

    def on_age_group_selection_changed(self, age_group_id, name):
        self.breadcrumb_age_group_label.setText(name)
        if not age_group_id:
            return
        self.update_domain_list()

    def on_domain_selection_changed(self, domain_id, name):
        self.breadcrumb_domain_label.setText(name)
        if self.age_group_list.currentRow() < 0:
            return
        if not domain_id:
            return
        self.update_body_list()

    def on_add_subject_clicked(self):
        if not self.age_group_list.current_id or not self.domain_list.current_id:
            return
        selected_age_group_idx = self.age_group_list.currentRow()
        selected_domain_idx = self.domain_list.currentRow()
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
        selected_age_group_idx = self.age_group_list.currentRow()
        selected_domain_idx = self.domain_list.currentRow()
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
        row_age = self.age_group_list.currentRow()
        row_domain = self.domain_list.currentRow()
        if row_age < 0 or row_domain < 0:
            return
        try:
            domain = self.settings["age_groups"][row_age]["domains"][row_domain]
            subject = next(
                (s for s in domain["subjects"] if s["id"] == subject_id), None
            )
            if subject:
                dn = domain["name"] or "dn"
                prefix = f"{row_age + 1}-{dn[0].upper()}"
                metric_data["code"] = f"{prefix}.{len(subject['metrics']) + 1}"
                subject["metrics"].append(metric_data)
                for i in range(self.body_list.count()):
                    item = self.body_list.item(i)
                    widget = self.body_list.itemWidget(item)
                    if widget and widget.subject_id == subject_id:
                        widget.updateTable(subject["metrics"])
                        item.setSizeHint(widget.sizeHint())
                        break
        except (IndexError, KeyError):
            return

    def on_delete_metric(self, subject_id, metric_id):
        selected_age_group_idx = self.age_group_list.currentRow()
        selected_domain_idx = self.domain_list.currentRow()
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
        self.domain_list.clear()

        selected_domain_idx = selected_domain_idx or 0

        row_age = self.age_group_list.currentRow()
        if row_age < 0:
            return
        age_group = self.settings["age_groups"][row_age]
        domains = age_group["domains"]

        # Fill the domain list
        for domain in domains:
            self.domain_list.addItem(
                domain["id"],
                domain["name"],
                "domain_item_widget",
                self.on_edit_domain,
                self.on_delete_domain,
            )

        # Update visibility and selection based on the new list of domains
        if len(domains) < 1:
            self.domain_list.setEmpty("Бағыттар жоқ")
            self.breadcrumb_domain_label.setText("")
            self.body_header_frame.setVisible(False)
            self.body_list.setVisible(False)
            self.body_empty_label.setText("Бағыттар жоқ")
            self.body_empty_label.setVisible(True)
            self.body_list.clear()
        else:
            selected_domain_idx = min(selected_domain_idx, len(domains) - 1)
            self.domain_list.setEmpty("", show=False)
            self.breadcrumb_domain_label.setText(domains[selected_domain_idx]["name"])
            self.body_header_frame.setVisible(True)
            self.body_list.setVisible(True)
            self.body_empty_label.setVisible(False)
            self.domain_list.setCurrentRow(selected_domain_idx)

        self.update_body_list()

    def update_body_list(self):
        self.body_list.clear()

        row_age = self.age_group_list.currentRow()
        row_domain = self.domain_list.currentRow()

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
        self.age_group_list.blockSignals(True)
        selected_age_group_idx = (
            selected_age_group_idx if selected_age_group_idx is not None else 0
        )
        selected_domain_idx = (
            selected_domain_idx if selected_domain_idx is not None else 0
        )
        self.age_group_list.clear()
        for age_group in settings["age_groups"]:
            self.age_group_list.addItem(
                age_group["id"],
                age_group["name"],
                "age_group_item_widget",
                self.on_edit_age_group,
                self.on_delete_age_group,
            )
        if len(settings["age_groups"]) < 1:
            self.age_group_list.setEmpty("Жас топтары жоқ")
            self.domain_list.setEmpty("Жас топтары жоқ")
            self.body_header_frame.setVisible(False)
            self.body_list.setVisible(False)
            self.body_empty_label.setText("Жас топтары жоқ")
            self.body_empty_label.setVisible(True)
            self.breadcrumb_age_group_label.setText("")
            self.breadcrumb_domain_label.setText("")
            self.domain_list.clear()
            self.body_list.clear()
            return
        selected_age_group_idx = min(
            selected_age_group_idx, len(settings["age_groups"]) - 1
        )
        self.age_group_list.setEmpty("", show=False)
        self.body_header_frame.setVisible(True)
        self.body_list.setVisible(True)
        self.body_empty_label.setVisible(False)
        self.breadcrumb_age_group_label.setText(
            settings["age_groups"][selected_age_group_idx]["name"]
        )
        self.age_group_list.blockSignals(False)
        self.age_group_list.setCurrentRow(selected_age_group_idx)

        self.update_domain_list(selected_domain_idx=selected_domain_idx)

    def get_data(self):
        return {
            "age_groups": self.settings["age_groups"],
        }
