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
from gui.models.settings_store import SettingsStore


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.store = SettingsStore(settings)
        self.setup_ui()
        self.connect_signals()
        self.refresh_all()

    def setup_ui(self):
        self.setWindowTitle("Баптаулар")
        self.setMinimumSize(950, 650)

        # SIDEBAR
        self.age_group_list = SimpleListWidget("Жас топтары")
        self.domain_list = SimpleListWidget("Бағыттар")

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
        self.body_header_frame.setFixedHeight(40)
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

        body_frame = QFrame()
        body_frame.setObjectName("settings_body_frame")
        body_layout = QVBoxLayout(body_frame)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(self.body_header_frame, 0)
        body_layout.addWidget(self.body_list, 1)
        body_layout.addWidget(self.body_empty_label, 1)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(sidebar_frame)
        layout.addWidget(body_frame)

    def connect_signals(self):
        self.age_group_list.on_selection_changed_signal.connect(
            self.handle_age_group_change
        )
        self.domain_list.on_selection_changed_signal.connect(self.handle_domain_change)

        self.age_group_list.on_add_signal.connect(self.on_add_age_group_clicked)
        self.domain_list.on_add_signal.connect(self.on_add_domain_clicked)

    def sync_subjects(self):
        self.body_list.clear()
        ag_idx = self.age_group_list.currentRow()
        dom_idx = self.domain_list.currentRow()

        subjects = self.store.get_subjects(ag_idx, dom_idx) if dom_idx >= 0 else []
        has_data = len(subjects) > 0

        self.body_header_frame.setVisible(dom_idx >= 0)
        self.body_list.setVisible(has_data)
        self.body_empty_label.setVisible(not has_data)

        if not has_data:
            msg = "Пәндер жоқ" if dom_idx >= 0 else "Бағыт таңдалмады"
            self.body_empty_label.setText(msg)
            return

        for sub in subjects:
            self._add_subject_to_list(sub)

    def sync_domains(self):
        self.domain_list.blockSignals(True)
        self.domain_list.clear()

        ag_idx = self.age_group_list.currentRow()
        domains = self.store.get_domains(ag_idx) if ag_idx >= 0 else []

        if not domains:
            msg = "Бағыттар жоқ" if ag_idx >= 0 else "Жас тобы таңдалмады"
            self.domain_list.setEmpty(msg)
        else:
            for dom in domains:
                self.domain_list.addItem(
                    dom["id"],
                    dom["name"],
                    "domain_item_widget",
                    self.on_edit_domain,
                    self.on_delete_domain,
                )
            self.domain_list.setEmpty("", show=False)

        self.domain_list.blockSignals(False)

        if domains:
            self.domain_list.setCurrentRow(0)
        else:
            self.sync_subjects()

    def refresh_all(self):
        self.age_group_list.blockSignals(True)
        self.age_group_list.clear()

        age_groups = self.store.get_age_groups()
        for ag in age_groups:
            self.age_group_list.addItem(
                ag["id"],
                ag["name"],
                "age_group_item_widget",
                self.on_edit_age_group,
                self.on_delete_age_group,
            )

        self.age_group_list.blockSignals(False)

        if age_groups:
            self.age_group_list.setCurrentRow(0)
        else:
            self.sync_domains()

    def handle_age_group_change(self, ag_id, name):
        self.breadcrumb_age_group_label.setText(name)
        self.sync_domains()

    def handle_domain_change(self, dom_id, name):
        self.breadcrumb_domain_label.setText(name)
        self.sync_subjects()

    @property
    def current_age_group(self):
        ag_id = self.age_group_list.current_id
        return self.store.find_ag(ag_id)

    @property
    def current_domain(self):
        ag = self.current_age_group
        dom_id = self.domain_list.current_id
        if ag and dom_id:
            return self.store.find_dom(ag["id"], dom_id)
        return None

    def _add_subject_to_list(self, subject):
        item = QListWidgetItem(self.body_list)
        custom_widget = SubjectBlock(subject["id"], subject["name"], subject["metrics"])
        item.setSizeHint(custom_widget.sizeHint())
        self.body_list.addItem(item)
        self.body_list.setItemWidget(item, custom_widget)
        custom_widget.on_delete_signal.connect(self.on_delete_subject)
        custom_widget.on_add_metric_signal.connect(self.on_add_metric)
        custom_widget.on_delete_metric_signal.connect(self.on_delete_metric)

    def get_data(self):
        return {
            "age_groups": self.store.settings["age_groups"],
        }

    # --- AGE GROUP ACTION HANDLERS ---

    def on_add_age_group_clicked(self):
        self.store.add_age_group()
        self.refresh_all()

    def on_edit_age_group(self, age_group_id, new_name):
        ag = self.store.find_ag(age_group_id)
        if ag:
            ag["name"] = new_name
        self.age_group_list.updateItemName(age_group_id, new_name)

        current_ag = self.current_age_group
        if current_ag and current_ag["id"] == age_group_id:
            self.breadcrumb_age_group_label.setText(new_name)

    def on_delete_age_group(self, age_group_id):
        self.store.delete_age_group(age_group_id)
        self.refresh_all()
        new_idx = max(0, self.age_group_list.currentRow())
        self.age_group_list.setCurrentRow(new_idx)

    # --- DOMAIN ACTION HANDLERS ---

    def on_add_domain_clicked(self):
        ag = self.current_age_group
        if ag:
            self.store.add_domain(ag["id"])
            self.sync_domains()

    def on_edit_domain(self, domain_id, new_name):
        ag = self.current_age_group
        if not ag:
            return
        dom = self.store.find_dom(ag["id"], domain_id)
        if not dom:
            return
        dom["name"] = new_name
        self.domain_list.updateItemName(domain_id, new_name)

        if self.domain_list.current_id == domain_id:
            self.breadcrumb_domain_label.setText(new_name)

    def on_delete_domain(self, domain_id):
        ag = self.current_age_group
        if not ag:
            return
        self.store.delete_domain(ag["id"], domain_id)
        self.sync_domains()
        new_idx = max(0, self.domain_list.currentRow())
        self.domain_list.setCurrentRow(new_idx)

    # --- SUBJECT ACTION HANDLERS ---

    def on_add_subject_clicked(self):
        ag = self.current_age_group
        dom = self.current_domain
        if ag and dom:
            self.store.add_subject(ag["id"], dom["id"])
            self.sync_subjects()
            self.body_list.scrollToBottom()

    def on_delete_subject(self, subject_id):
        ag = self.current_age_group
        if not ag:
            return
        dom = self.current_domain
        if not dom:
            return
        self.store.delete_subject(ag["id"], dom["id"], subject_id)

        for i in range(self.body_list.count()):
            item = self.body_list.item(i)
            widget = self.body_list.itemWidget(item)
            if widget and widget.subject_id == subject_id:
                self.body_list.takeItem(i)
                break

        self.sync_subjects()

    # --- METRIC ACTION HANDLERS ---

    def on_add_metric(self, subject_id):
        ag = self.current_age_group
        if not ag:
            return
        dom = self.current_domain
        if not dom:
            return
        sub = self.store.find_sub(ag["id"], dom["id"], subject_id)
        if not sub:
            return

        ag_idx = self.age_group_list.currentRow()
        dn = dom.get("name", "X")
        prefix = f"{ag_idx + 1}-{dn[0].upper()}"
        self.store.add_metric(ag["id"], dom["id"], sub["id"], prefix)

        for i in range(self.body_list.count()):
            item = self.body_list.item(i)
            widget = self.body_list.itemWidget(item)
            if widget and widget.subject_id == subject_id:
                widget.updateTable(sub["metrics"])
                item.setSizeHint(widget.sizeHint())
                break

    def on_delete_metric(self, subject_id, metric_id):
        ag = self.current_age_group
        if not ag:
            return
        dom = self.current_domain
        if not dom:
            return
        sub = self.store.find_sub(ag["id"], dom["id"], subject_id)
        if not sub:
            return
        self.store.delete_metric(ag["id"], dom["id"], sub["id"], metric_id)

        for i in range(self.body_list.count()):
            item = self.body_list.item(i)
            widget = self.body_list.itemWidget(item)
            if widget and widget.subject_id == subject_id:
                widget.updateTable(sub["metrics"])
                item.setSizeHint(widget.sizeHint())
                break
