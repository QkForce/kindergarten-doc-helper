from PySide6.QtWidgets import (
    QLabel,
    QPlainTextEdit,
)

from gui.dialogs.base_dialog import BaseDialog


class DomainDialog(BaseDialog):
    def __init__(self, name, placeholder_key, title="ЖАҢА ДОМЕН ҚОСУ", parent=None):
        super().__init__(title, parent)
        self.setFixedSize(500, 350)

        name_label = QLabel("АТАУЫ")
        name_label.setProperty("lbl-level", "label")
        self.name_edit = QPlainTextEdit()
        self.name_edit.setPlainText(name)

        placeholder_key_label = QLabel("ШАБЛОНДАҒЫ МАРКЕР")
        placeholder_key_label.setProperty("lbl-level", "label")
        self.placeholder_key_edit = QPlainTextEdit()
        self.placeholder_key_edit.setPlainText(placeholder_key)

        self.body_layout.setContentsMargins(25, 20, 25, 20)
        self.body_layout.addWidget(name_label)
        self.body_layout.addWidget(self.name_edit)
        self.body_layout.addWidget(placeholder_key_label)
        self.body_layout.addWidget(self.placeholder_key_edit)

    def getResult(self) -> dict:
        return {
            "name": self.name_edit.toPlainText().strip(),
            "placeholder_key": self.placeholder_key_edit.toPlainText().strip(),
        }

    def isEmpty(self) -> bool:
        return not bool(self.name_edit.toPlainText().strip()) or not bool(
            self.placeholder_key_edit.toPlainText().strip()
        )
