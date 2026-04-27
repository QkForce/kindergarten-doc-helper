from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)


class AgeGroupItemWidget(QFrame):
    def __init__(self, id, name, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setObjectName("age_group_item_widget")
        self.setProperty("selected", "false")
        self.id = id
        self.name = name

        self.label = QLabel(self.name)
        self.label.setWordWrap(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addSpacing(0)
        layout.addWidget(self.label)
        layout.addStretch()

    def setActive(self, is_active):
        self.setProperty("selected", "true" if is_active else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        self.update()
