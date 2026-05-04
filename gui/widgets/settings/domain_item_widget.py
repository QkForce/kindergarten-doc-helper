from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import Signal

from gui.constants.icons import IconPaths
from gui.widgets.icon_button import IconButton


class DomainItemWidget(QFrame):
    on_delete_signal = Signal(str)  # domain ID

    def __init__(self, id, name, parent=None):
        super().__init__(parent)
        self.setObjectName("domain_item_widget")
        self.setProperty("selected", "false")
        self.id = id
        self.name = name

        self.label = QLabel(self.name)
        self.label.setWordWrap(True)

        delete_btn = IconButton(IconPaths.TRASH, icon_size=12)
        delete_btn.setProperty("btn-type", "ghost")
        delete_btn.setFixedSize(16, 16)
        delete_btn.clicked.connect(lambda: self.on_delete_signal.emit(self.id))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addSpacing(0)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(delete_btn)

    def setActive(self, is_active):
        self.setProperty("selected", "true" if is_active else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        self.update()
