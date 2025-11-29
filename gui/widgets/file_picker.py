import os
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QFrame,
)
from PySide6.QtCore import Qt, Signal


class FilePickerWidget(QWidget):
    fileSelected = Signal(str)

    def __init__(
        self,
        label_text="Мониторинг файлы",
        btn_text="Файлды таңдау",
        caption="Excel файлын таңдау",
        dir="",
        filter="Excel Files (*.xlsx *.xlsm)",
        parent=None,
    ):
        super().__init__(parent)
        self.caption = caption
        self.dir = dir
        self.filter = filter

        self.title_label = QLabel(label_text)
        self.title_label.setProperty("lbl-level", "lbl")

        self.file_select_frame = QFrame(self)
        self.file_select_frame.setProperty("frame-style", "box")
        self.file_select_frame.setFrameShape(QFrame.Box)
        self.file_select_frame.setLineWidth(1)

        self.btn_browse = QPushButton(btn_text)
        self.btn_browse.setProperty("btn-type", "neutral")
        self.btn_browse.setProperty("btn-size", "small")
        self.btn_browse.clicked.connect(self.pick_file)

        self.file_label = QLabel("Файл таңдалмаған")
        self.file_label.setProperty("lbl-level", "p")
        self.file_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.frame_layout = QHBoxLayout()
        self.frame_layout.addWidget(self.btn_browse)
        self.frame_layout.addSpacing(10)
        self.frame_layout.addWidget(self.file_label)
        self.frame_layout.addStretch()
        self.file_select_frame.setLayout(self.frame_layout)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.title_label)
        layout.addWidget(self.file_select_frame)

    def pick_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.caption, self.dir, self.filter
        )
        if file_path:
            self.file_label.setText(os.path.basename(file_path))
            self.fileSelected.emit(file_path)
        else:
            self.file_label.setText("Файл таңдалмады")
            self.fileSelected.emit("")

    def setEnabled(self, arg__1):
        self.btn_browse.setEnabled(arg__1)
        btn_type = "neutral" if arg__1 else "disabled"
        self.btn_browse.setProperty("btn-type", btn_type)
        self.btn_browse.style().polish(self.btn_browse)
        return super().setEnabled(arg__1)
