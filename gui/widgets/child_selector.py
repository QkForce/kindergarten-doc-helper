from typing import List, Tuple

from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Signal

from gui.widgets.items.child_item import ChildItemWidget, AssessmentStatus


class ChildSelector(QFrame):
    children_name_list = []
    childSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("child_selector")
        self.setFixedWidth(250)

        title = QLabel("Балалар тізімі")
        title.setProperty("lbl-level", "h3")
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.addWidget(title)
        title_layout.addStretch()

        self.list_widget = QListWidget()
        self.list_widget.setFrameShape(QFrame.NoFrame)
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.addLayout(title_layout)
        layout.addWidget(self.list_widget)

    def applyData(self, children: List[Tuple[str, AssessmentStatus]]):
        self.list_widget.clear()
        self.children_name_list = [child[0] for child in children]
        for i, (name, status) in enumerate(children):
            item = QListWidgetItem(self.list_widget)
            custom_widget = ChildItemWidget(f"{i+1}. {name}", status)
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
                self.childSelected.emit(self.children_name_list[i])

    def setChildStatus(self, child_name, status: AssessmentStatus):
        index = (
            self.children_name_list.index(child_name)
            if child_name in self.children_name_list
            else -1
        )
        if index == -1:
            return
        item = self.list_widget.item(index)
        widget = self.list_widget.itemWidget(item)
        print(f"Setting status for {child_name} to {status}")
        widget.setStatus(status)
