from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QAbstractItemView,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt

from gui.widgets.reorderable_table_widget import ReorderableTableWidget


class SortChildrenContent(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("sort_children_content")

        sub_title = QLabel("Балалар тізімі:")
        sub_title.setProperty("lbl-level", "h3")

        self.table = ReorderableTableWidget()
        self.table.setShowGrid(False)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setCornerButtonEnabled(False)
        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.setDropIndicatorShown(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setDragDropMode(QAbstractItemView.InternalMove)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            [
                "Баланың аты-жөні",
                "Туған күні",
                "Бастапқы (X-XII)",
                "Аралық (II-IV)",
                "Қорытынды (VI-VIII)",
            ]
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(sub_title)
        layout.addWidget(self.table)

    def set_table_item(self, row, fullname, birth_date, start, mid, end):
        self.table.setItem(row, 0, QTableWidgetItem(str(fullname)))
        self.table.setItem(row, 1, QTableWidgetItem(str(birth_date)))
        self.table.setItem(row, 2, QTableWidgetItem(start))
        self.table.setItem(row, 3, QTableWidgetItem(str(mid)))
        self.table.setItem(row, 4, QTableWidgetItem(str(end)))

    def applyData(self, children=None):
        if children is not None:
            self.children = children

        self.table.setRowCount(len(self.children))

        for row, child in enumerate(self.children):
            assessments = child.get("assessments", [])
            start_assessments = [
                next(iter(a["criterion"]), "")
                for a in assessments
                if len(a["start"]) > 1
            ]
            mid_assessments = [
                next(iter(a["criterion"]), "") for a in assessments if len(a["mid"]) > 1
            ]
            end_assessments = [
                next(iter(a["criterion"]), "") for a in assessments if len(a["end"]) > 1
            ]
            self.set_table_item(
                row,
                child.get("fullname", ""),
                child.get("birth_date", ""),
                ", ".join(start_assessments),
                ", ".join(mid_assessments),
                ", ".join(end_assessments),
            )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.table.setColumnWidth(0, 260)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        for i in range(2, self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
