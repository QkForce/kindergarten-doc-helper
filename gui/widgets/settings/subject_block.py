import time

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from gui.constants.colors import AppColors
from gui.constants.icons import IconPaths
from gui.utils.icon_utils import get_svg_pixmap
from gui.widgets.icon_button import IconButton


class SubjectBlock(QFrame):
    on_add_metric_signal = Signal(str, dict)  # subject ID, metric data
    on_delete_signal = Signal(str)  # subject ID

    def __init__(self, id, name, metrics, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_subject_block")
        self.subject_id = id
        self.subject_name = name
        self.metrics = metrics

        self.title = QLabel(self.subject_name)

        add_metric_btn = QPushButton("+ Метрика қосу")
        add_metric_btn.setProperty("btn-size", "small")
        add_metric_btn.setProperty("btn-type", "link")
        add_metric_btn.setFixedHeight(26)
        add_metric_btn.clicked.connect(
            lambda: self.on_add_metric_signal.emit(
                self.subject_id,
                {
                    "id": f"metric_{time.time_ns()}",
                    "code": "",
                    "transformed": "",
                    "criteria": ["", "", ""],
                },
            )
        )

        delete_icon = get_svg_pixmap(
            IconPaths.TRASH, AppColors.BTN_ICON_DANGER_CONTENT, 14
        )
        delete_btn = IconButton(
            IconPaths.TRASH,
            icon_size=14,
            current_color=AppColors.BTN_ICON_DANGER_CONTENT,
            hover_color=AppColors.BTN_ICON_DANGER_HOVER_BG,
        )
        delete_btn.setIcon(QIcon(delete_icon))
        delete_btn.setProperty("btn-type", "ghost")
        delete_btn.setFixedSize(26, 26)
        delete_btn.setToolTip("Пәнді жою")
        delete_btn.clicked.connect(lambda: self.on_delete_signal.emit(self.subject_id))

        header_frame = QFrame()
        header_frame.setObjectName("settings_subject_block_header")
        header_layout = QHBoxLayout(header_frame)
        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(add_metric_btn)
        header_layout.addWidget(delete_btn)

        self.table = QTableWidget()
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.verticalHeader().hide()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "Код",
                "Метирика сипаттамасы",
                "Критерия (Жақсы)",
                "Критерия (Орташа)",
                "Критерия (Нашар)",
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

    def updateTable(self, metrics=None):
        if metrics is not None:
            self.metrics = metrics
        self.table.setRowCount(len(self.metrics))
        for row, metric in enumerate(self.metrics):
            criteria = metric.get("criteria", ["", "", ""])
            self.table.setItem(row, 0, QTableWidgetItem(str(metric.get("code", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(metric.get("transformed", "")))
            self.table.setItem(row, 2, QTableWidgetItem(str(criteria[0])))
            self.table.setItem(row, 3, QTableWidgetItem(str(criteria[1])))
            self.table.setItem(row, 4, QTableWidgetItem(str(criteria[2])))
        header = self.table.horizontalHeader()
        for i in range(0, self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

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
