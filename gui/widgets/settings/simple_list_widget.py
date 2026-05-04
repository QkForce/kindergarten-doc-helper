from PySide6.QtWidgets import (
    QFrame,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Qt, Signal

from gui.constants.icons import IconPaths
from gui.widgets.settings.simple_list_item_widget import SimpleListItemWidget
from gui.widgets.icon_button import IconButton


class SimpleListWidget(QFrame):
    on_add_signal = Signal()
    on_selection_changed_signal = Signal(
        str, str
    )  # Emits the ID and name of the selected item

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setObjectName("simple_list_widget")

        title_lbl = QLabel(title)
        title_lbl.setFixedHeight(40)
        title_lbl.setObjectName("sidebar_title")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        add_btn = IconButton(IconPaths.CIRCLE_PLUS, icon_size=12)
        add_btn.setProperty("btn-type", "ghost")
        add_btn.setFixedSize(16, 16)
        add_btn.clicked.connect(self.on_add_signal.emit)

        header_layout = QHBoxLayout()
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(add_btn)
        header_layout.addSpacing(8)

        self.list = QListWidget()
        # self.list.setFixedHeight(160)
        self.list.itemSelectionChanged.connect(self.on_selection_changed)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.empty_label = QLabel("Тізім бос")
        self.empty_label.setFixedHeight(30)
        self.empty_label.setObjectName("empty_list_label")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setVisible(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(header_layout, 0)
        layout.addWidget(self.list, 0)
        layout.addWidget(self.empty_label, 0)

    @property
    def current_id(self):
        row = self.list.currentRow()
        if row < 0:
            return None
        item = self.list.item(row)
        widget = self.list.itemWidget(item)
        return widget.id if widget else None

    def currentRow(self):
        return self.list.currentRow()

    def setCurrentRow(self, row):
        self.list.setCurrentRow(row)

    def on_selection_changed(self):
        if self.list.currentRow() < 0:
            self.on_selection_changed_signal.emit("", "")
            return

        selected_items = self.list.selectedItems()
        for i in range(self.list.count()):
            item = self.list.item(i)
            widget = self.list.itemWidget(item)
            if widget:
                is_active = item in selected_items
                widget.setActive(is_active)
                if is_active:
                    self.on_selection_changed_signal.emit(widget.id, widget.name)

    def setEmpty(self, text, show=True):
        self.empty_label.setText(text)
        self.empty_label.setVisible(show)
        self.list.setVisible(not show)

    def addItem(self, id, name, obj_name, on_edit, on_delete, width=180):
        item = QListWidgetItem(self.list)
        custom_widget = SimpleListItemWidget(id, name, obj_name)
        custom_widget.setFixedWidth(width)
        item.setSizeHint(custom_widget.sizeHint())
        self.list.addItem(item)
        self.list.setItemWidget(item, custom_widget)
        custom_widget.on_edit_signal.connect(on_edit)
        custom_widget.on_delete_signal.connect(
            lambda: self.on_delete_clicked(custom_widget.id, on_delete)
        )

        self.empty_label.setVisible(False)
        self.list.setVisible(True)

        # self.list.blockSignals(True)
        # item.setSelected(True)
        # custom_widget.setActive(True)
        # self.list.blockSignals(False)

    def deleteItem(self, id):
        target_row = -1
        for i in range(self.list.count()):
            widget = self.list.itemWidget(self.list.item(i))
            if widget and widget.id == id:
                target_row = i
                break
        if target_row != -1:
            self.list.takeItem(target_row)
            if self.list.count() == 0:
                self.setEmpty("Тізім бос", show=True)

    def clear(self):
        self.list.blockSignals(True)
        self.list.clear()
        self.list.blockSignals(False)

    def on_delete_clicked(self, id, on_delete):
        self.deleteItem(id)
        on_delete(id)
