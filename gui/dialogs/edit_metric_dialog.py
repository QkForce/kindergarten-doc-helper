from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QFrame,
)
from PySide6.QtCore import Qt

from gui.constants.icons import IconPaths
from gui.constants.colors import AppColors
from gui.widgets.icon_button import IconButton


class EditMetricDialog(QDialog):
    def __init__(self, met_id, code, desc, c1, c2, c3, parent=None):
        super().__init__(parent)
        self.Accepted = QDialog.Accepted
        self._drag_pos = None
        self.setWindowTitle("Индикаторды (метрика) өзгерту")
        self.setFixedSize(700, 650)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # --- Header ---
        title = QLabel("МЕТРИКАНЫ ӨҢДЕУ")
        title.setProperty("lbl-level", "h3")

        close_btn = IconButton(
            IconPaths.CLOSE,
            icon_size=16,
            current_color=AppColors.BTN_ICON_DANGER_CONTENT,
            hover_color=AppColors.BTN_ICON_DANGER_HOVER_BG,
        )
        close_btn.setProperty("btn-type", "ghost")
        close_btn.setFixedSize(24, 24)
        close_btn.setCursor(Qt.CursorShape.ArrowCursor)
        close_btn.clicked.connect(self.reject)

        self.header = QFrame()
        self.header.setFixedHeight(60)
        self.header.setCursor(Qt.CursorShape.OpenHandCursor)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)

        # Separator line
        line = QFrame()
        line.setObjectName("separator")
        line.setFrameShape(QFrame.Shape.HLine)

        # --- Body ---
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

        line2 = QFrame()
        line2.setObjectName("separator")
        line2.setFrameShape(QFrame.Shape.HLine)

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

        body = QFrame()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(25, 20, 25, 20)
        body_layout.addLayout(code_desc_layout)
        body_layout.addSpacing(30)
        body_layout.addWidget(line2)
        body_layout.addWidget(c1_lbl)
        body_layout.addWidget(self.c1_input)
        body_layout.addWidget(c2_lbl)
        body_layout.addWidget(self.c2_input)
        body_layout.addWidget(c3_lbl)
        body_layout.addWidget(self.c3_input)

        # --- Footer ---
        cancel_btn = QPushButton("Болдырмау")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setProperty("btn-size", "large")
        cancel_btn.setProperty("btn-type", "ghost")
        cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("Сақтау")
        self.save_btn.setFixedSize(120, 40)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setProperty("btn-size", "large")
        self.save_btn.setProperty("btn-type", "primary")
        self.save_btn.clicked.connect(self.accept)

        footer = QFrame()
        footer.setFixedHeight(80)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(25, 0, 25, 0)
        footer_layout.setSpacing(15)
        footer_layout.addStretch()
        footer_layout.addWidget(cancel_btn)
        footer_layout.addWidget(self.save_btn)

        # content layout
        container_frame = QFrame(self)
        container_frame.setObjectName("dialogContainer")
        container_frame.setProperty("frame-style", "dialog")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container_frame)
        content_layout = QVBoxLayout(container_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        content_layout.addWidget(self.header)
        content_layout.addWidget(line)
        content_layout.addWidget(body)
        content_layout.addStretch()
        content_layout.addWidget(footer)

    def getData(self):
        return {
            "code": self.code_input.toPlainText().strip(),
            "desc": self.desc_input.toPlainText().strip(),
            "c1": self.c1_input.toPlainText().strip(),
            "c2": self.c2_input.toPlainText().strip(),
            "c3": self.c3_input.toPlainText().strip(),
        }

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.header.underMouse():
                self.header.setCursor(Qt.CursorShape.ClosedHandCursor)
                self._drag_pos = event.globalPosition().toPoint()
                event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.header.setCursor(Qt.CursorShape.OpenHandCursor)
        self._drag_pos = None
        event.accept()
