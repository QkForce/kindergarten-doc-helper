from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

from gui.dialogs.name_dialog import NameDialog
from gui.dialogs.domain_dialog import DomainDialog
from gui.widgets.settings.age_group_list_item_widget import AgeGroupListItemWidget
from gui.widgets.settings.domain_list_item_widget import DomainListItemWidget
from gui.widgets.settings.simple_list_widget import SimpleListWidget
from gui.widgets.settings.subject_list_widget import SubjectListWidget
from gui.models.settings_store import SettingsStore


class SettingsDialog(QDialog):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.store = SettingsStore(settings)
        self.setup_ui()
        self.connect_signals()
        self.refresh_all()
        self.age_group_list.selectFirstItem()

    def setup_ui(self):
        self.setWindowTitle("Баптаулар")
        self.setMinimumSize(950, 650)

        # SIDEBAR
        ag_dialog = lambda parent: NameDialog("", "Жаңа жас тобын қосу", parent)
        self.age_group_list = SimpleListWidget("Жас топтары", ag_dialog)

        dom_dialog = lambda parent: DomainDialog("", "", "Жаңа бағыт қосу", parent)
        self.domain_list = SimpleListWidget("Бағыттар", dom_dialog)

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
        self.body = SubjectListWidget("Жаңа пән қосу")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(sidebar_frame)
        layout.addWidget(self.body)

    def connect_signals(self):
        self.age_group_list.on_selection_changed_signal.connect(
            self.handle_age_group_change
        )
        self.domain_list.on_selection_changed_signal.connect(self.handle_domain_change)

        self.age_group_list.on_add_signal.connect(self.on_add_age_group_clicked)
        self.domain_list.on_add_signal.connect(self.on_add_domain_clicked)
        self.body.on_add_subject_signal.connect(self.on_add_subject_clicked)

    def sync_subjects(self):
        self.body.clear()

        ag_idx = self.age_group_list.currentRow()
        if ag_idx < 0:
            self.body.setEmpty(
                "Жас тобы таңдалмады немесе жас тобы тізімі бос", hide_header=True
            )
            return

        dom_idx = self.domain_list.currentRow()
        if dom_idx < 0:
            self.body.setEmpty(
                "Бағыт таңдалмады немесе бағыт тізімі бос", hide_header=True
            )
            return

        subjects = self.store.get_subjects(ag_idx, dom_idx)
        if len(subjects) == 0:
            self.body.setEmpty("Пәндер жоқ", hide_header=False)
            return

        for sub in subjects:
            self.body.addSubject(
                sub,
                self.on_edit_subject,
                self.on_delete_subject,
                self.on_add_metric,
                self.on_edit_metric,
                self.on_delete_metric,
            )

    def sync_domains(self):
        self.domain_list.clear()

        ag_idx = self.age_group_list.currentRow()
        if ag_idx < 0:
            self.domain_list.setEmpty("Жас тобы таңдалмады немесе жас тобы тізімі бос")
            self.body.setEmpty(
                "Жас тобы таңдалмады немесе жас тобы тізімі бос", hide_header=True
            )
            return

        domains = self.store.get_domains(ag_idx)
        if len(domains) == 0:
            self.domain_list.setEmpty("Бағыттар жоқ")
            return

        for dom in domains:
            item_widget = DomainListItemWidget(
                dom["id"],
                dom["name"],
                dom["placeholder_key"],
                "domain_item_widget",
                self.on_edit_domain,
                self.on_delete_domain,
                parent=self.domain_list,
            )
            self.domain_list.addItem(item_widget)

    def refresh_all(self):
        self.age_group_list.blockSignals(True)
        self.age_group_list.clear()

        age_groups = self.store.get_age_groups()
        for ag in age_groups:
            item_widget = AgeGroupListItemWidget(
                ag["id"],
                ag["name"],
                "age_group_item_widget",
                self.on_edit_age_group,
                self.on_delete_age_group,
                parent=self.age_group_list,
            )
            self.age_group_list.addItem(item_widget)

        self.age_group_list.blockSignals(False)

    def handle_age_group_change(self, ag_id, name):
        self.body.setBreadcrumbAgeGroup(name)
        self.sync_domains()
        self.domain_list.selectFirstItem()

    def handle_domain_change(self, dom_id, name):
        self.body.setBreadcrumbDomain(name)
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

    def get_data(self):
        return {
            "age_groups": self.store.settings["age_groups"],
        }

    # --- AGE GROUP ACTION HANDLERS ---

    def on_add_age_group_clicked(self, dialog_result):
        ag = self.store.add_age_group(dialog_result["name"])
        item_widget = AgeGroupListItemWidget(
            ag["id"],
            ag["name"],
            "age_group_item_widget",
            self.on_edit_age_group,
            self.on_delete_age_group,
            parent=self.age_group_list,
        )
        self.age_group_list.addItem(item_widget)
        self.age_group_list.selectLastItem()

    def on_edit_age_group(self, age_group_id, result):
        new_name = result["name"]
        ag = self.store.find_ag(age_group_id)
        if ag:
            ag["name"] = new_name
        self.age_group_list.updateItemData(age_group_id, {"name": new_name})

        current_ag = self.current_age_group
        if current_ag and current_ag["id"] == age_group_id:
            self.body.setBreadcrumbAgeGroup(new_name)

    def on_delete_age_group(self, age_group_id):
        self.store.delete_age_group(age_group_id)
        self.age_group_list.deleteItem(age_group_id)
        new_idx = max(0, self.age_group_list.currentRow())
        self.age_group_list.setCurrentRow(new_idx)

    # --- DOMAIN ACTION HANDLERS ---

    def on_add_domain_clicked(self, dialog_result):
        ag = self.current_age_group
        if ag:
            dom = self.store.add_domain(
                ag["id"], dialog_result["name"], dialog_result["placeholder_key"]
            )
            item_widget = DomainListItemWidget(
                dom["id"],
                dom["name"],
                dom["placeholder_key"],
                "domain_item_widget",
                self.on_edit_domain,
                self.on_delete_domain,
                parent=self.domain_list,
            )
            self.domain_list.addItem(item_widget)
            self.domain_list.selectLastItem()

    def on_edit_domain(self, domain_id, result):
        new_name = result["name"]
        ag = self.current_age_group
        if not ag:
            return
        dom = self.store.find_dom(ag["id"], domain_id)
        if not dom:
            return
        dom["name"] = new_name
        dom["placeholder_key"] = result["placeholder_key"]
        self.domain_list.updateItemData(
            domain_id, {"name": new_name, "placeholder_key": result["placeholder_key"]}
        )

        if self.domain_list.current_id == domain_id:
            self.body.setBreadcrumbDomain(new_name)

    def on_delete_domain(self, domain_id):
        ag = self.current_age_group
        if not ag:
            return
        self.store.delete_domain(ag["id"], domain_id)
        self.domain_list.deleteItem(domain_id)
        new_idx = max(0, self.domain_list.currentRow())
        self.domain_list.setCurrentRow(new_idx)

    # --- SUBJECT ACTION HANDLERS ---

    def on_add_subject_clicked(self, name):
        ag = self.current_age_group
        dom = self.current_domain
        if ag and dom:
            sub = self.store.add_subject(ag["id"], dom["id"], name)
            self.body.addSubject(
                sub,
                self.on_edit_subject,
                self.on_delete_subject,
                self.on_add_metric,
                self.on_edit_metric,
                self.on_delete_metric,
            )
            self.body.scrollToBottom()

    def on_edit_subject(self, sub_id, new_name):
        ag = self.current_age_group
        if not ag:
            return
        dom = self.current_domain
        if not dom:
            return
        self.store.edit_subject(ag["id"], dom["id"], sub_id, new_name)

        self.body.editSubject(sub_id, new_name)

    def on_delete_subject(self, subject_id):
        ag = self.current_age_group
        if not ag:
            return
        dom = self.current_domain
        if not dom:
            return
        self.store.delete_subject(ag["id"], dom["id"], subject_id)

        self.body.deleteSubject(subject_id)

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

        self.body.updateMetrics(subject_id, sub["metrics"])

    def on_edit_metric(self, subject_id, met_id, new_data):
        ag = self.current_age_group
        if not ag:
            return
        dom = self.current_domain
        if not dom:
            return
        sub = self.store.find_sub(ag["id"], dom["id"], subject_id)
        if not sub:
            return
        self.store.edit_metric(ag["id"], dom["id"], sub["id"], met_id, new_data)

        self.body.updateMetrics(subject_id, sub["metrics"])

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

        self.body.updateMetrics(subject_id, sub["metrics"])
