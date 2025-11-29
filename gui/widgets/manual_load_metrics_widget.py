from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Signal

from gui.utils.form_utils import create_vertical_field


class ManualLoadMetricsWidget(QWidget):
    manual_load_clicked = Signal(int, int, int, int)

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout(self)
        main_v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()

        metric_code_row_layout, metric_code_row_input = create_vertical_field(
            "Метрика кодының жолы:"
        )
        metric_description_row_layout, metric_description_row_input = (
            create_vertical_field("Метрика сипаттамасының жолы:")
        )
        metrics_start_col_layout, metrics_start_col_input = create_vertical_field(
            "Бағана басы:"
        )
        metrics_end_col_layout, metrics_end_col_input = create_vertical_field(
            "Бағана аяғы:"
        )
        self.metric_code_row_input = metric_code_row_input
        self.metric_description_row_input = metric_description_row_input
        self.metrics_start_col_input = metrics_start_col_input
        self.metrics_end_col_input = metrics_end_col_input
        h_layout.addLayout(metric_code_row_layout)
        h_layout.addLayout(metric_description_row_layout)
        h_layout.addLayout(metrics_start_col_layout)
        h_layout.addLayout(metrics_end_col_layout)

        self.load_btn = QPushButton("Жүктеу")
        self.load_btn.setProperty("btn-type", "danger")
        self.load_btn.setProperty("btn-size", "large")
        self.load_btn.clicked.connect(self.on_manual_load)

        main_v_layout.addLayout(h_layout)
        main_v_layout.addWidget(self.load_btn)
        self.layout.addLayout(main_v_layout)

    def on_manual_load(self):
        metric_code_row = int(self.metric_code_row_input.text())
        metric_description_row = int(self.metric_description_row_input.text())
        metrics_start_col = int(self.metrics_start_col_input.text())
        metrics_end_col = int(self.metrics_end_col_input.text())
        self.manual_load_clicked.emit(
            metric_code_row,
            metric_description_row,
            metrics_start_col,
            metrics_end_col,
        )
