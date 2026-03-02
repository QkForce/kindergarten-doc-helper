from PySide6.QtWidgets import (
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Signal

from gui.widgets.items.child_item import ChildItemWidget


class ChildSelector(QFrame):
    childSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("frame-style", "sidebar")
        self.setFixedWidth(250)

        layout = QVBoxLayout(self)

        title = QLabel("Балалар тізімі")
        title.setProperty("lbl-level", "h3")
        layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.setFrameShape(QFrame.NoFrame)
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.list_widget.setObjectName("child_selector")

        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.list_widget)

    def set_data(self, children_names):
        self.list_widget.clear()
        for name in children_names:
            item = QListWidgetItem(self.list_widget)
            custom_widget = ChildItemWidget(name)
            item.setSizeHint(custom_widget.sizeHint())

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, custom_widget)

    def _on_selection_changed(self):
        selected_items = self.list_widget.selectedItems()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            widget.setSelected(item in selected_items)
            if item in selected_items:
                self.childSelected.emit(widget.name_label.text())
