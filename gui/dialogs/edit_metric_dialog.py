from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QFrame,
)

from gui.dialogs.base_dialog import BaseDialog


class EditMetricDialog(BaseDialog):
    def __init__(self, met_id, code, desc, c1, c2, c3, parent=None):
        super().__init__("МЕТРИКАНЫ ӨҢДЕУ", parent)
        self.setFixedSize(700, 650)
        self.metric_id = met_id

        code_lbl = QLabel("КОД")
        code_lbl.setProperty("lbl-level", "label")
        self.code_input = QPlainTextEdit()
        self.code_input.setFixedWidth(60)
        self.code_input.setPlainText(code)
        code_layout = QVBoxLayout()
        code_layout.addWidget(code_lbl)
        code_layout.addWidget(self.code_input)

        desc_lbl = QLabel("ИНДИКАТОР СИПАТТАМАСЫ")
        desc_lbl.setProperty("lbl-level", "label")
        self.desc_input = QPlainTextEdit()
        self.desc_input.setPlainText(desc)
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(desc_lbl)
        desc_layout.addWidget(self.desc_input)

        code_desc_layout = QHBoxLayout()
        code_desc_layout.addLayout(code_layout)
        code_desc_layout.addLayout(desc_layout)

        line = QFrame()
        line.setObjectName("separator")
        line.setFrameShape(QFrame.Shape.HLine)

        c1_lbl = QLabel("1-ДЕҢГЕЙ КРИТЕРИЙІ")
        c1_lbl.setProperty("lbl-level", "label")
        self.c1_input = QPlainTextEdit()
        self.c1_input.setPlainText(c1)

        c2_lbl = QLabel("2-ДЕҢГЕЙ КРИТЕРИЙІ")
        c2_lbl.setProperty("lbl-level", "label")
        self.c2_input = QPlainTextEdit()
        self.c2_input.setPlainText(c2)

        c3_lbl = QLabel("3-ДЕҢГЕЙ КРИТЕРИЙІ")
        c3_lbl.setProperty("lbl-level", "label")
        self.c3_input = QPlainTextEdit()
        self.c3_input.setPlainText(c3)

        self.body_layout.setContentsMargins(25, 20, 25, 20)
        self.body_layout.addLayout(code_desc_layout)
        self.body_layout.addSpacing(30)
        self.body_layout.addWidget(line)
        self.body_layout.addWidget(c1_lbl)
        self.body_layout.addWidget(self.c1_input)
        self.body_layout.addWidget(c2_lbl)
        self.body_layout.addWidget(self.c2_input)
        self.body_layout.addWidget(c3_lbl)
        self.body_layout.addWidget(self.c3_input)

    def getData(self):
        return {
            "met_id": self.metric_id,
            "code": self.code_input.toPlainText().strip(),
            "desc": self.desc_input.toPlainText().strip(),
            "c1": self.c1_input.toPlainText().strip(),
            "c2": self.c2_input.toPlainText().strip(),
            "c3": self.c3_input.toPlainText().strip(),
        }
