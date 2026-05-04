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


class RenameDialog(QDialog):
    def __init__(self, current_name, parent=None):
        super().__init__(parent)
        self.Accepted = QDialog.Accepted
        self.setWindowTitle("Атауды өзгерту")
        self.setFixedSize(500, 350)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # --- Header ---
        title_label = QLabel("АТАУДЫ ӨЗГЕРТУ")
        title_label.setProperty("lbl-level", "h3")

        close_btn = IconButton(
            IconPaths.CLOSE,
            icon_size=16,
            current_color=AppColors.BTN_ICON_DANGER_CONTENT,
            hover_color=AppColors.BTN_ICON_DANGER_HOVER_BG,
        )
        close_btn.setProperty("btn-type", "ghost")
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(self.reject)

        header = QFrame()
        header.setFixedHeight(60)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)

        # Separator line
        line = QFrame()
        line.setObjectName("separator")
        line.setFrameShape(QFrame.Shape.HLine)
        # line.setFixedHeight(1)

        # --- Body ---
        input_label = QLabel("АТАУЫ")
        input_label.setProperty("lbl-level", "label")

        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlainText(current_name)

        body = QFrame()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(25, 20, 25, 20)
        body_layout.addWidget(input_label)
        body_layout.addWidget(self.text_edit)

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

        content_layout.addWidget(header)
        content_layout.addWidget(line)
        content_layout.addWidget(body)
        content_layout.addStretch()
        content_layout.addWidget(footer)

    def getText(self):
        return self.text_edit.toPlainText().strip()
