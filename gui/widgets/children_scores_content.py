from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QHeaderView,
    QHeaderView,
    QLabel,
)
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from gui.widgets.frozen_table import FrozenTable


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
                item = QStandardItem(self._convert_score(value))
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
        self.table.resizeColumnsToContents()
        self.table.setup_columns_visibility()

    def _convert_score(self, value):
        if value == 1:
            return "✅"
        elif value == 2 or value == 3:
            return "*"
        else:
            return "_"
