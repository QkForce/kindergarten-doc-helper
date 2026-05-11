from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QWidget,
)
from PySide6.QtCore import Qt, Signal

from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.dialogs.name_dialog import NameDialog
from gui.dialogs.edit_metric_dialog import EditMetricDialog
from gui.widgets.icon_button import IconButton


class SubjectBlock(QFrame):
    on_edit_signal = Signal(str, str)  # subject ID, new name
    on_delete_signal = Signal(str)  # subject ID
    on_add_metric_signal = Signal(str)  # subject ID
    on_edit_metric_signal = Signal(str, str, dict)  # subject ID, metric ID, metric data
    on_delete_metric_signal = Signal(str, str)  # subject ID, metric ID

    def __init__(self, id, name, metrics, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_subject_block")
        self.subject_id = id
        self.subject_name = name
        self.metrics = metrics

        self.title = QLabel(self.subject_name)

        edit_btn = IconButton(
            IconPaths.EDIT,
            icon_size=12,
        )
        edit_btn.setProperty("btn-type", "ghost")
        edit_btn.setFixedSize(26, 26)
        edit_btn.clicked.connect(self.on_edit_clicked)

        add_metric_btn = QPushButton("+ Метрика қосу")
        add_metric_btn.setProperty("btn-size", "small")
        add_metric_btn.setProperty("btn-type", "link")
        add_metric_btn.setFixedHeight(26)
        add_metric_btn.clicked.connect(
            lambda: self.on_add_metric_signal.emit(self.subject_id)
        )

        delete_btn = IconButton(
            IconPaths.TRASH,
            icon_size=14,
            current_color=AppColors.BTN_ICON_DANGER_CONTENT,
            hover_color=AppColors.BTN_ICON_DANGER_HOVER_BG,
        )
        delete_btn.setProperty("btn-type", "ghost")
        delete_btn.setFixedSize(26, 26)
        delete_btn.setToolTip("Пәнді жою")
        delete_btn.clicked.connect(lambda: self.on_delete_signal.emit(self.subject_id))

        header_frame = QFrame()
        header_frame.setObjectName("settings_subject_block_header")
        header_layout = QHBoxLayout(header_frame)
        header_layout.addWidget(self.title)
        header_layout.addSpacing(10)
        header_layout.addWidget(edit_btn)
        header_layout.addStretch()
        header_layout.addWidget(add_metric_btn)
        header_layout.addWidget(delete_btn)

        self.table = QTableWidget()
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().hide()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            [
                "Код",
                "Метирика сипаттамасы",
                "Критерия (Жақсы)",
                "Критерия (Орташа)",
                "Критерия (Нашар)",
                "Әрекеттер",
            ]
        )

        self.metrics_empty_label = QLabel("Метрикалар жоқ")
        self.metrics_empty_label.setObjectName("empty_list_label")
        self.metrics_empty_label.setFixedHeight(50)
        self.metrics_empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.metrics_empty_label.hide()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(header_frame, 0)
        layout.addWidget(self.table, 1)
        layout.addWidget(self.metrics_empty_label, 1)

        self.updateTable()

    def set_table_item(self, row, met_id, code, desc, c1, c2, c3):
        self.table.setItem(row, 0, QTableWidgetItem(str(code)))
        self.table.setItem(row, 1, QTableWidgetItem(desc))
        self.table.setItem(row, 2, QTableWidgetItem(str(c1)))
        self.table.setItem(row, 3, QTableWidgetItem(str(c2)))
        self.table.setItem(row, 4, QTableWidgetItem(str(c3)))

        edit_btn = IconButton(
            IconPaths.EDIT,
            icon_size=14,
        )
        edit_btn.setProperty("btn-type", "ghost")
        edit_btn.setToolTip("Метриканы өзгерту")
        edit_btn.clicked.connect(
            lambda checked=False, m_id=met_id: self.on_edit_metric_clicked(
                m_id, code, desc, c1, c2, c3
            )
        )

        delete_btn = IconButton(
            IconPaths.TRASH,
            icon_size=14,
            current_color=AppColors.BTN_ICON_DANGER_CONTENT,
            hover_color=AppColors.BTN_ICON_DANGER_HOVER_BG,
        )
        delete_btn.setProperty("btn-type", "ghost")
        delete_btn.setToolTip("Метриканы жою")
        delete_btn.clicked.connect(
            lambda checked=False, m_id=met_id: self.on_delete_metric_signal.emit(
                self.subject_id, m_id
            )
        )

        oper_frame = QFrame()
        oper_cell = QHBoxLayout(oper_frame)
        oper_cell.setContentsMargins(0, 0, 0, 0)
        oper_cell.addWidget(edit_btn)
        oper_cell.addWidget(delete_btn)
        self.table.setCellWidget(row, 5, oper_frame)

    def updateTable(self, metrics=None):
        if metrics is not None:
            self.metrics = metrics
        self.table.setRowCount(len(self.metrics))
        for row, metric in enumerate(self.metrics):
            criteria = metric.get("criteria", ["", "", ""])
            self.set_table_item(
                row,
                metric.get("id", ""),
                metric.get("code", ""),
                metric.get("transformed", ""),
                criteria[0],
                criteria[1],
                criteria[2],
            )
        header = self.table.horizontalHeader()
        for i in range(0, self.table.columnCount() - 1):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(
            self.table.columnCount() - 1, QHeaderView.ResizeMode.ResizeToContents
        )

        # Calculate height
        total_height = self.table.horizontalHeader().height()
        for i in range(self.table.rowCount()):
            total_height += self.table.rowHeight(i)
        total_height += self.table.frameWidth() * 2
        self.table.setFixedHeight(total_height)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Empty state
        metrics_empty = len(self.metrics) == 0
        self.metrics_empty_label.setVisible(metrics_empty)

    def setSubjectName(self, name):
        self.subject_name = name
        self.title.setText(name)

    def on_edit_clicked(self):
        dialog = NameDialog(self.subject_name, "АТАУДЫ ӨЗГЕРТУ", self)
        if dialog.exec() == dialog.Accepted:
            new_name = dialog.getText()
            if new_name:
                self.on_edit_signal.emit(self.subject_id, new_name)

    def on_edit_metric_clicked(self, met_id, code, desc, c1, c2, c3):
        dialog = EditMetricDialog(met_id, code, desc, c1, c2, c3)
        if dialog.exec() == dialog.Accepted:
            new_data = dialog.getData()
            self.on_edit_metric_signal.emit(self.subject_id, met_id, new_data)
