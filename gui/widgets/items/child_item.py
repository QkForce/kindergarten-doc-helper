from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)


class ChildItemWidget(QWidget):
    def __init__(self, name, status="empty", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        # Status marker (circle)
        self.status_icon = QLabel()
        self.setStatus(status)

        # Child's name
        self.name_label = QLabel(name)
        self.name_label.setObjectName("child_name_label")

        layout.addWidget(self.status_icon)
        layout.addWidget(self.name_label)
        layout.addStretch()

    def setStatus(self, status):
        icons = {
            "success": "🟢",
            "partial": "🟡",
            "empty": "⚪",
        }
        self.status_icon.setText(icons.get(status, "⚪"))
