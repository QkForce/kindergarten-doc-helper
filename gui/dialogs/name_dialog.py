from PySide6.QtWidgets import (
    QLabel,
    QPlainTextEdit,
)

from gui.dialogs.base_dialog import BaseDialog


class NameDialog(BaseDialog):
    def __init__(self, name, title="АТАУДЫ ӨЗГЕРТУ", parent=None):
        super().__init__(title, parent)
        self.setFixedSize(500, 350)

        input_label = QLabel("АТАУЫ")
        input_label.setProperty("lbl-level", "label")

        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlainText(name)

        self.body_layout.setContentsMargins(25, 20, 25, 20)
        self.body_layout.addWidget(input_label)
        self.body_layout.addWidget(self.text_edit)

    def getResult(self) -> dict:
        return {"name": self.text_edit.toPlainText().strip()}

    def isEmpty(self) -> bool:
        return not bool(self.text_edit.toPlainText().strip())
