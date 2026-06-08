from PySide6.QtWidgets import (
    QFrame,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.dialogs.name_dialog import NameDialog
from gui.utils.icon_utils import get_svg_pixmap
from gui.widgets.settings.subject_block import SubjectBlock


class SubjectListWidget(QFrame):
    on_add_subject_signal = Signal(str)  # name
    on_edit_subject_signal = Signal(str, str)  # id, new name

    def __init__(self, add_title, parent=None):
        super().__init__(parent)
        self.add_title = add_title
        self.setup_ui()

    def setup_ui(self):
        self.age_group_label = QLabel()
        self.age_group_label.setObjectName("breadcrumb_label")
        self.age_group_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        chevron_pixmap = get_svg_pixmap(IconPaths.CHEVRON_RIGHT, AppColors.PRIMARY, 14)
        chevron_icon = QLabel()
        chevron_icon.setPixmap(chevron_pixmap)
        chevron_icon.setObjectName("breadcrumb_chevron_icon")
        self.domain_label = QLabel()
        self.domain_label.setObjectName("breadcrumb_label")
        self.domain_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        add_subject_btn = QPushButton("  Пән қосу")
        add_subject_btn.setProperty("btn-size", "small")
        add_subject_btn.setProperty("btn-type", "primary")
        add_icon = get_svg_pixmap(IconPaths.PLUS, AppColors.CANVAS, 14)
        add_subject_btn.setIcon(QIcon(add_icon))
        add_subject_btn.setFixedHeight(26)
        add_subject_btn.clicked.connect(self.on_add_subject_clicked)

        self.header_frame = QFrame()
        self.header_frame.setObjectName("header_frame")
        self.header_frame.setFixedHeight(40)
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(10, 6, 10, 6)
        header_layout.setSpacing(8)
        header_layout.addWidget(self.age_group_label)
        header_layout.addWidget(chevron_icon)
        header_layout.addWidget(self.domain_label)
        header_layout.addStretch()
        header_layout.addWidget(add_subject_btn)

        self.list = QListWidget()
        self.list.setObjectName("settings_subjects_list")

        self.empty_label = QLabel("")
        self.empty_label.setObjectName("empty_list_label")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setVisible(False)

        layout = QVBoxLayout(self)
        self.setObjectName("settings_body_frame")
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.header_frame, 0)
        layout.addWidget(self.list, 1)
        layout.addWidget(self.empty_label, 1)

    # --- event handlers ---

    def on_add_subject_clicked(self):
        dialog = NameDialog("", self.add_title, self)
        if dialog.exec() == dialog.Accepted:
            if not dialog.isEmpty():
                result = dialog.getResult()
                self.on_add_subject_signal.emit(result["name"])

    # --- BREADCRUMB METHODS ---

    def setBreadcrumbAgeGroup(self, ag_name):
        self.age_group_label.setText(ag_name)

    def setBreadcrumbDomain(self, dom_name):
        self.domain_label.setText(dom_name)

    # --- LIST METHODS ---

    def scrollToBottom(self):
        self.list.scrollToBottom()

    def clear(self):
        self.list.clear()

    # --- EMPTY STATE ---

    def setEmpty(self, msg, hide_header=False):
        self.header_frame.setVisible(not hide_header)
        self.list.setVisible(False)
        self.empty_label.setText(msg)
        self.empty_label.setVisible(True)

    # --- SUBJECT METHODS ---

    def addSubject(
        self,
        sub,
        on_edit_subject,
        on_delete_subject,
        on_add_metric,
        on_edit_metric,
        on_delete_metric,
    ):
        item = QListWidgetItem(self.list)
        custom_widget = SubjectBlock(sub["id"], sub["name"], sub["metrics"])
        item.setSizeHint(custom_widget.sizeHint())
        self.list.addItem(item)
        self.list.setItemWidget(item, custom_widget)

        custom_widget.on_edit_signal.connect(on_edit_subject)
        custom_widget.on_delete_signal.connect(on_delete_subject)
        custom_widget.on_add_metric_signal.connect(on_add_metric)
        custom_widget.on_edit_metric_signal.connect(on_edit_metric)
        custom_widget.on_delete_metric_signal.connect(on_delete_metric)

        self.list.setVisible(True)
        self.empty_label.setVisible(False)

    def editSubject(self, sub_id, new_name):
        for i in range(self.list.count()):
            item = self.list.item(i)
            widget = self.list.itemWidget(item)
            if widget and widget.subject_id == sub_id:
                widget.setSubjectName(new_name)
                break

    def deleteSubject(self, subject_id):
        for i in range(self.list.count()):
            item = self.list.item(i)
            widget = self.list.itemWidget(item)
            if widget and widget.subject_id == subject_id:
                old_item = self.list.takeItem(i)
                del old_item
                break
        if self.list.count() == 0:
            self.setEmpty("Пәндер жоқ")

    # --- METRIC METHODS ---

    def updateMetrics(self, sub_id, metrics):
        for i in range(self.list.count()):
            item = self.list.item(i)
            widget = self.list.itemWidget(item)
            if widget and widget.subject_id == sub_id:
                widget.updateTable(metrics)
                item.setSizeHint(widget.sizeHint())
                break
