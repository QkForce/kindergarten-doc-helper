from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
)


class DomainItemWidget(QFrame):
    def __init__(self, id, name, parent=None):
        super().__init__(parent)
        self.setObjectName("domain_item_widget")
        self.setProperty("selected", "false")
        self.id = id
        self.name = name

        self.label = QLabel(self.name)
        self.label.setWordWrap(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.addWidget(self.label)

    def setActive(self, is_active):
        self.setProperty("selected", "true" if is_active else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        self.update()
