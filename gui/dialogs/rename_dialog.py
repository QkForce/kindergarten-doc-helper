from PySide6.QtWidgets import (
    QLabel,
    QPlainTextEdit,
)

from gui.dialogs.base_dialog import BaseDialog


class RenameDialog(BaseDialog):
    def __init__(self, current_name, parent=None):
        super().__init__("АТАУДЫ ӨЗГЕРТУ", parent)
        self.setFixedSize(500, 350)

        input_label = QLabel("АТАУЫ")
        input_label.setProperty("lbl-level", "label")

        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlainText(current_name)

        self.body_layout.setContentsMargins(25, 20, 25, 20)
        self.body_layout.addWidget(input_label)
        self.body_layout.addWidget(self.text_edit)

    def getText(self):
        return self.text_edit.toPlainText().strip()
