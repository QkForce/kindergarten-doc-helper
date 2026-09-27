from typing import List, Tuple

from PySide6.QtWidgets import (
    QListView,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QFrame,
)
from PySide6.QtCore import Qt, Signal

from logic.types import AssessmentStatus
from ..components.selector_item import SelectorItem


class DomainSelector(QFrame):
    domainSelected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.domain_name_list = []
        self.setObjectName("domain_selector")
        self.setFixedHeight(100)

        title = QLabel("Даму бағытын таңдаңыз:")
        title.setProperty("lbl-level", "h3")
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.addWidget(title)
        title_layout.addStretch()

        self.list_widget = QListWidget()
        self.list_widget.setSpacing(4)
        self.list_widget.setFlow(QListView.Flow.LeftToRight)
        self.list_widget.setWrapping(False)
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.list_widget.setResizeMode(QListView.Adjust)
        self.list_widget.setHorizontalScrollMode(QListWidget.ScrollPerPixel)
        self.list_widget.itemSelectionChanged.connect(self._on_selection_changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addLayout(title_layout)
        layout.addWidget(self.list_widget)

    def applyData(self, domains: List[Tuple[str, str, AssessmentStatus]]):
        self.list_widget.clear()
        self.domain_name_list = [dom[0] for dom in domains]
        for i, (name, dom_name, status) in enumerate(domains):
            item = QListWidgetItem(self.list_widget)
            custom_widget = SelectorItem(f"{i+1}. {dom_name} ", status)
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
                self.domainSelected.emit(self.domain_name_list[i])

    def selectDomain(self, domain_name):
        index = (
            self.domain_name_list.index(domain_name)
            if domain_name in self.domain_name_list
            else -1
        )
        if index == -1:
            return
        item = self.list_widget.item(index)
        self.list_widget.setCurrentItem(item)

    def setDomainStatus(self, domain_name, status: AssessmentStatus):
        index = (
            self.domain_name_list.index(domain_name)
            if domain_name in self.domain_name_list
            else -1
        )
        if index == -1:
            return
        item = self.list_widget.item(index)
        widget = self.list_widget.itemWidget(item)
        widget.setStatus(status)
