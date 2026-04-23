from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)

from gui.constants.strings import DOMAIN_NAMES


class DomainItemWidget(QFrame):
    def __init__(self, domain_key, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setObjectName("domain_item_widget")
        self.setProperty("selected", "false")
        self.domain_key = domain_key
        self.domain_name = DOMAIN_NAMES[domain_key]

        self.label = QLabel(self.domain_name)
        self.label.setWordWrap(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.addWidget(self.label)
        layout.addStretch()

    def setActive(self, is_active):
        self.setProperty("selected", "true" if is_active else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
