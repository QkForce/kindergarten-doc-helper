from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QHeaderView,
    QLabel,
)
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from gui.widgets.frozen_table import FrozenTable

FIRST_COL_WIDTH = 170
CELL_WIDTH = 25


class ChildrenScoresWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        sub_title = QLabel("Балалардың метрика бойынша бағалары:")
        sub_title.setProperty("lbl-level", "h3")

        self.model = QStandardItemModel()
        self.table = FrozenTable(self.model)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QTableView.NoEditTriggers)

        self.lbl_status = QLabel(f"Бос бағалар:")
        self.lbl_status.setProperty("lbl-level", "h3")

        layout.addWidget(sub_title)
        layout.addWidget(self.table)
        layout.addWidget(self.lbl_status)
        self.setContentsMargins(0, 0, 0, 0)

    def set_data(self, children_scores, metric_codes):
        headers = ["Баланың аты-жөні"] + metric_codes
        self.model.clear()
        self.model.setHorizontalHeaderLabels(headers)

        has_errors = False
        for child in children_scores:
            row = []
            row.append(QStandardItem(child["name"]))
            for code in metric_codes:
                value = child.get(code, -1)
                item = QStandardItem(str(value) if value > 0 else "")
                item.setData(value, Qt.UserRole)
                if value < 1:
                    color = QColor(255, 230, 230)
                    has_errors = True
                else:
                    color = QColor(230, 255, 230)
                item.setBackground(color)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                row.append(item)
            self.model.appendRow(row)
        self.has_errors = has_errors

        header = self.table.horizontalHeader()

        # Make the first column resizable by the user (Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)

        self.table.setColumnWidth(0, FIRST_COL_WIDTH)
        header.setMinimumSectionSize(CELL_WIDTH)

        # Resize the remaining columns to fit their contents
        for i in range(1, self.model.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.table.setup_columns_visibility()
