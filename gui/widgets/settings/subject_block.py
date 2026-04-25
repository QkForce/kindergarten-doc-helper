from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt

from gui.constants.strings import SUBJECT_NAMES


class SubjectBlock(QFrame):
    def __init__(self, subject_key, metrics, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_subject_block")
        self.subject_key = subject_key
        self.subject_name = SUBJECT_NAMES[subject_key]
        self.metrics = metrics

        self.title = QLabel(self.subject_name)
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.addWidget(self.title)
        header_layout.addStretch()

        self.table = QTableWidget()
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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(header_frame, 0)
        layout.addWidget(self.table, 1)

        self.updateTable()

    def updateTable(self):
        self.table.setRowCount(len(self.metrics))
        for row, (code, metric) in enumerate(self.metrics.items()):
            criteria = metric.get("criteria", ["", "", ""])
            self.table.setItem(row, 0, QTableWidgetItem(str(code)))
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
