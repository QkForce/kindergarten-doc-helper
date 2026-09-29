from typing import List

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Signal

from logic.types import AssessmentStatus, SelectorItemDTO
from gui.steps.step_child_assessment.components.selector_item import SelectorItem


class LeftBarSelector(QFrame):
    itemSelected = Signal(str)

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.item_id_list: list[str] = []
        self.setObjectName("left_bar_selector")
        self.setFixedWidth(250)

        title_lbl = QLabel(title)
        title_lbl.setProperty("lbl-level", "h3")
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.addWidget(title_lbl)
        title_layout.addStretch()

        self.list_widget = QListWidget()
        self.list_widget.setFrameShape(QFrame.NoFrame)
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.addLayout(title_layout)
        layout.addWidget(self.list_widget)

    def applyData(self, list_data: List[SelectorItemDTO]):
        self.list_widget.clear()
        self.item_id_list = [row["id"] for row in list_data]
        for row in list_data:
            item = QListWidgetItem(self.list_widget)
            custom_widget = SelectorItem(row["title"], parent=self.list_widget)
            item.setSizeHint(custom_widget.sizeHint())

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, custom_widget)

    def _on_selection_changed(self):
        selected_items = self.list_widget.selectedItems()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            if widget:
                widget.setSelected(item in selected_items)
            if item in selected_items:
                self.itemSelected.emit(self.item_id_list[i])

    def selectItem(self, item_id: str):
        index = self.item_id_list.index(item_id) if item_id in self.item_id_list else -1
        if index == -1:
            return
        item = self.list_widget.item(index)
        self.list_widget.setCurrentItem(item)

    def setItemStatus(self, item_id: str, status: AssessmentStatus):
        index = self.item_id_list.index(item_id) if item_id in self.item_id_list else -1
        if index == -1:
            return
        item = self.list_widget.item(index)
        widget = self.list_widget.itemWidget(item)
        if widget:
            widget.setStatus(status)
