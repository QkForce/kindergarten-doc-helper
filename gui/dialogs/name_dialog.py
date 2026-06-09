from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
)

from gui.dialogs.base_dialog import BaseDialog


class NameDialog(BaseDialog):
    def __init__(self, name, title="АТАУДЫ ӨЗГЕРТУ", parent=None):
        super().__init__(title, parent)
        self.setFixedSize(500, 350)

        input_label = QLabel("АТАУЫ")
        input_label.setProperty("lbl-level", "lbl")

        self.text_edit = QLineEdit()
        self.text_edit.setText(name)

        self.body_layout.setContentsMargins(25, 20, 25, 20)
        self.body_layout.addWidget(input_label)
        self.body_layout.addWidget(self.text_edit)
        self.body_layout.addStretch(1)

    def getResult(self) -> dict:
        return {"name": self.text_edit.text().strip()}

    def isEmpty(self) -> bool:
        return not bool(self.text_edit.text().strip())
