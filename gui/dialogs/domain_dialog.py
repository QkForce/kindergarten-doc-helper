from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
)

from gui.dialogs.base_dialog import BaseDialog


class DomainDialog(BaseDialog):
    def __init__(self, name, placeholder_key, title="ЖАҢА ДОМЕН ҚОСУ", parent=None):
        super().__init__(title, parent)
        self.setFixedSize(500, 350)

        name_label = QLabel("АТАУЫ")
        name_label.setProperty("lbl-level", "lbl")
        self.name_edit = QLineEdit()
        self.name_edit.setText(name)

        placeholder_key_label = QLabel("ШАБЛОНДАҒЫ МАРКЕР")
        placeholder_key_label.setProperty("lbl-level", "lbl")
        self.placeholder_key_edit = QLineEdit()
        self.placeholder_key_edit.setText(placeholder_key)

        self.body_layout.setContentsMargins(25, 20, 25, 20)
        self.body_layout.addWidget(name_label)
        self.body_layout.addWidget(self.name_edit)
        self.body_layout.addWidget(placeholder_key_label)
        self.body_layout.addWidget(self.placeholder_key_edit)
        self.body_layout.addStretch(1)

    def getResult(self) -> dict:
        return {
            "name": self.name_edit.text().strip(),
            "placeholder_key": self.placeholder_key_edit.text().strip(),
        }

    def isEmpty(self) -> bool:
        return not bool(self.name_edit.text().strip()) or not bool(
            self.placeholder_key_edit.text().strip()
        )
