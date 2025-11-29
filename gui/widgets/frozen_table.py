from PySide6.QtWidgets import QTableView, QAbstractItemView
from PySide6.QtCore import Qt, QItemSelectionModel, QSize


class FrozenTable(QTableView):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setModel(model)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.verticalHeader().hide()

        # Создаём frozen_table (первая колонка)
        self.frozen_table = QTableView(self)
        self.frozen_table.setModel(model)
        self.frozen_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.frozen_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.frozen_table.verticalHeader().hide()
        self.frozen_table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.frozen_table.horizontalHeader().setFixedHeight(35)
        self.horizontalHeader().setFixedHeight(35)

        # Синхронизация прокрутки
        self.verticalScrollBar().valueChanged.connect(
            self.frozen_table.verticalScrollBar().setValue
        )
        self.frozen_table.verticalScrollBar().valueChanged.connect(
            self.verticalScrollBar().setValue
        )

        # Синхронизация выделения
        self.selectionModel().currentRowChanged.connect(self._sync_selection)
        self.frozen_table.selectionModel().currentRowChanged.connect(
            self._sync_frozen_selection
        )

        # Синхронизация ширины первого столбца
        self.horizontalHeader().sectionResized.connect(self._on_section_resized)

        # Показываем заголовки
        self.horizontalHeader().show()
        self.horizontalHeader().setStretchLastSection(False)
        self.frozen_table.horizontalHeader().show()
        self.frozen_table.horizontalHeader().setStretchLastSection(False)

        # overlay поверх содержимого
        self.frozen_table.raise_()

    def _sync_selection(self, current, previous):
        if current.isValid():
            self.frozen_table.selectionModel().setCurrentIndex(
                self.model().index(current.row(), 0),
                QItemSelectionModel.SelectionFlag.Select
                | QItemSelectionModel.SelectionFlag.Rows
                | QItemSelectionModel.SelectionFlag.Current,
            )

    def _sync_frozen_selection(self, current, previous):
        if current.isValid():
            self.selectionModel().setCurrentIndex(
                self.model().index(current.row(), 1),
                QItemSelectionModel.SelectionFlag.Select
                | QItemSelectionModel.SelectionFlag.Rows
                | QItemSelectionModel.SelectionFlag.Current,
            )

    def _on_section_resized(self, logicalIndex, oldSize, newSize):
        if logicalIndex in (0, 1):
            self.updateFrozenTableGeometry()

    def setup_columns_visibility(self):
        for i in range(1, self.model().columnCount()):
            self.frozen_table.hideColumn(i)
        self.updateFrozenTableGeometry()

    def updateFrozenTableGeometry(self):
        if not self.horizontalHeader().count():
            return
        col_width = self.horizontalHeader().sectionSize(0)
        header_height = self.horizontalHeader().height()
        h = self.viewport().height() + header_height
        self.frozen_table.setGeometry(0, 0, col_width, h)
        self.frozen_table.setColumnWidth(0, col_width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateFrozenTableGeometry()

    def setShowGrid(self, show):
        super().setShowGrid(show)
        self.frozen_table.setShowGrid(show)

    def showEvent(self, event):
        return super().showEvent(event)
