from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Signal
from gui.utils.form_utils import create_vertical_field


class ManualLoadChildrenWidget(QWidget):
    manual_load_clicked = Signal(int, int, int)

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        main_v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        col_layout, col_input = create_vertical_field("Аты-жөні бағаны:")
        row_start_layout, row_start_input = create_vertical_field("Бастапқы жол:")
        row_end_layout, row_end_input = create_vertical_field("Соңғы жол:")
        self.col_input = col_input
        self.row_start_input = row_start_input
        self.row_end_input = row_end_input
        h_layout.addLayout(col_layout)
        h_layout.addLayout(row_start_layout)
        h_layout.addLayout(row_end_layout)

        self.load_btn = QPushButton("Жүктеу")
        self.load_btn.setProperty("btn-type", "danger")
        self.load_btn.setProperty("btn-size", "large")
        self.load_btn.clicked.connect(self.on_manual_load)

        main_v_layout.addLayout(h_layout)
        main_v_layout.addWidget(self.load_btn)
        self.layout.addLayout(main_v_layout)

    def on_manual_load(self):
        name_col = int(self.col_input.text())
        start_row = int(self.row_start_input.text())
        end_row = int(self.row_end_input.text())
        self.manual_load_clicked.emit(start_row, end_row, name_col)
