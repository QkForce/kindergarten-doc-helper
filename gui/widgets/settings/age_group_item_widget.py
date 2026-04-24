from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)

from gui.constants.strings import AGE_GROUPS


class AgeGroupItemWidget(QFrame):
    def __init__(self, age_group_key, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setObjectName("age_group_item_widget")
        self.setProperty("selected", "false")
        self.age_group_key = age_group_key
        self.age_group_name = AGE_GROUPS[age_group_key]

        self.label = QLabel(self.age_group_name)
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
