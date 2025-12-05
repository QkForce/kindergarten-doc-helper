from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QFrame,
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QGuiApplication, QIcon


class EditRowDialog(QDialog):
    saveItem = Signal(int, str, str)

    def __init__(self, parent, metrics, mapping, start_row=0):
        super().__init__(parent)

        self.metrics = metrics
        self.mapping = mapping
        self.current_row = start_row

        self.setWindowTitle("Метрика сипаттамасын өңдеу")
        self.setFixedWidth(600)
        self.setMinimumHeight(400)
        # self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        # Code
        lbl_code_key = QLabel("Excel-дегі метрика коды: ")
        lbl_code_key.setProperty("lbl-level", "lbl")
        self.lbl_code_value = QLabel()
        self.lbl_code_value.setProperty("lbl-level", "p")
        code_layout = QHBoxLayout()
        code_layout.addWidget(lbl_code_key)
        code_layout.addWidget(self.lbl_code_value, alignment=Qt.AlignLeft)
        code_layout.addStretch()

        # Description
        lbl_desc_key = QLabel("Excel-дегі метрика сипаттамасы: ")
        lbl_desc_key.setProperty("lbl-level", "lbl")
        self.lbl_desc_value = QLabel()
        self.lbl_desc_value.setWordWrap(True)
        self.lbl_desc_value.setProperty("lbl-level", "p")
        btn_copy_desc = QPushButton("Көшіру")
        btn_copy_desc.setProperty("btn-type", "neutral")
        btn_copy_desc.setProperty("btn-size", "small")
        btn_copy_desc.clicked.connect(
            lambda: self._copy_to_clipboard(self.lbl_desc_value.text())
        )
        btn_copy_desc.setIcon(QIcon("gui/resources/icons/content_copy.png"))
        btn_copy_desc.setIconSize(QSize(16, 16))
        desc_top_layout = QHBoxLayout()
        desc_top_layout.addWidget(lbl_desc_key)
        desc_top_layout.addStretch()
        desc_top_layout.addWidget(btn_copy_desc)
        desc_frame = QFrame()
        desc_frame.setLineWidth(1)
        desc_frame.setProperty("frame-style", "box")
        desc_frame.setFrameShape(QFrame.Box)
        desc_layout = QVBoxLayout(desc_frame)
        desc_layout.addLayout(desc_top_layout)
        desc_layout.addWidget(self.lbl_desc_value)

        # Transformed description
        lbl_transformed = QLabel("Docx-тегі метрика сипаттамасы:")
        lbl_transformed.setProperty("lbl-level", "lbl")
        self.edit_transformed = QTextEdit()
        self.edit_transformed.setProperty("textedit-style", "box")

        # Navigation buttons
        self.btn_prev = QPushButton("Алдыңғы")
        self.btn_prev.setProperty("btn-type", "neutral")
        self.btn_prev.setProperty("btn-size", "large")
        self.btn_prev.setIcon(QIcon("gui/resources/icons/arrow_back.png"))
        self.btn_prev.setIconSize(QSize(24, 24))
        self.btn_prev.setFixedHeight(40)

        self.btn_next = QPushButton("Келесі")
        self.btn_next.setProperty("btn-type", "neutral")
        self.btn_next.setProperty("btn-size", "large")
        self.btn_next.setLayoutDirection(Qt.RightToLeft)
        self.btn_next.setIcon(QIcon("gui/resources/icons/arrow_forward.png"))
        self.btn_next.setIconSize(QSize(24, 24))
        self.btn_next.setFixedHeight(40)

        self.btn_save_and_close = QPushButton("Уақытша сақтау және жабу")
        self.btn_save_and_close.setProperty("btn-type", "primary")
        self.btn_save_and_close.setProperty("btn-size", "large")
        self.btn_save_and_close.setFixedHeight(40)

        self.btn_prev.clicked.connect(self.go_prev)
        self.btn_next.clicked.connect(self.go_next)
        self.btn_save_and_close.clicked.connect(self.save_current)

        btn_nav = QHBoxLayout()
        btn_nav.addWidget(self.btn_prev)
        btn_nav.addWidget(self.btn_next)
        btn_nav.addStretch()
        btn_nav.addWidget(self.btn_save_and_close)

        layout = QVBoxLayout(self)
        layout.addLayout(code_layout)
        layout.addSpacing(10)
        layout.addWidget(desc_frame)
        layout.addSpacing(10)
        layout.addWidget(lbl_transformed)
        layout.addWidget(self.edit_transformed)
        layout.addSpacing(10)
        layout.addLayout(btn_nav)

        self.load_row(start_row)
        self.setContentsMargins(15, 15, 15, 15)

    # def closeEvent(self, event):
    #     event.ignore()

    def load_row(self, row):
        metric = self.metrics[row]
        code = metric["code"]
        description = metric["desc"]
        transformed = self.mapping[code]["transformed"]
        self.lbl_code_value.setText(code)
        self.lbl_desc_value.setText(description)
        self.edit_transformed.setPlainText(transformed)
        self.current_row = row
        self.update_nav_buttons()

    def go_prev(self):
        if self.current_row > 0:
            self.save_current(silent=True)
            self.load_row(self.current_row - 1)

    def go_next(self):
        if self.current_row < len(self.metrics) - 1:
            self.save_current(silent=True)
            self.load_row(self.current_row + 1)

    def save_current(self, silent=False):
        new_val = self.edit_transformed.toPlainText().strip()
        code = self.metrics[self.current_row]["code"]
        self.saveItem.emit(self.current_row, code, new_val)
        self.mapping[code]["transformed"] = new_val
        if not silent:
            self.accept()

    def update_nav_buttons(self):
        self.btn_prev.setEnabled(self.current_row > 0)
        self.btn_next.setEnabled(self.current_row < len(self.metrics) - 1)

    def _copy_to_clipboard(self, text: str):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)
