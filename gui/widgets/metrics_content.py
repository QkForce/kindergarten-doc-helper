from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from gui.dialogs.edit_row_dialog import EditRowDialog


class MetricsContent(QWidget):
    mappingChanged = Signal(str, str)  # code, new_transformed

    def __init__(self):
        super().__init__()
        sub_title = QLabel("Метрикалар:")
        sub_title.setProperty("lbl-level", "h3")

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.verticalHeader().hide()
        self.table.setShowGrid(False)
        self.table.setHorizontalHeaderLabels(
            ["Код", "Excel сипаттамасы", "Docx сипаттамасы (mapping)"]
        )
        self.table.setWordWrap(True)
        self.table.cellDoubleClicked.connect(self.open_edit_dialog)
        horizontal_header = self.table.horizontalHeader()
        horizontal_header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        horizontal_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        horizontal_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        horizontal_header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.btn_save = QPushButton("Mapping-ті дискіге сақтау")
        self.btn_save.setProperty("btn-type", "neutral")
        self.btn_save.setProperty("btn-size", "small")
        self.btn_save.clicked.connect(self.on_save)
        self.btn_save.setEnabled(False)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.btn_save)
        self.buttons_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.addWidget(sub_title)
        layout.addWidget(self.table)
        layout.addLayout(self.buttons_layout)

    def set_data(self, metrics, mapping):
        self.metrics = metrics
        self.mapping = mapping

        self.table.setRowCount(len(metrics))
        has_errors = False

        for i, metric in enumerate(metrics):
            code = metric["code"]
            excel_desc = metric["desc"]
            mapped_desc = (
                "" if mapping.get(code) is None else mapping.get(code)["transformed"]
            )

            item_code = QTableWidgetItem(code)
            item_excel = QTableWidgetItem(excel_desc)
            item_docx = QTableWidgetItem(mapped_desc if mapped_desc else "")

            if code not in mapping:
                color = QColor(255, 230, 230)  # bright red
                has_errors = True
            elif mapped_desc.strip() != excel_desc.strip():
                color = QColor(255, 255, 200)  # bright yellow
                has_errors = True
            else:
                color = QColor(230, 255, 230)  # bright green

            for item in [item_code, item_excel, item_docx]:
                item.setBackground(color)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                item.setToolTip("Өңдеу үшін екі рет шертіңіз!")
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignTop)

            self.table.setItem(i, 0, item_code)
            self.table.setItem(i, 1, item_excel)
            self.table.setItem(i, 2, item_docx)

        self.table.resizeRowsToContents()
        self.btn_save.setEnabled(not has_errors)

    def open_edit_dialog(self, row, column):
        dlg = EditRowDialog(self, self.metrics, self.mapping, start_row=row)
        dlg.saveItem.connect(self.update_row_from_dialog)
        if dlg.exec():
            self.revalidate_all_rows()

    def update_row_from_dialog(self, row, code, new_val):
        self.mapping[code]["transformed"] = new_val
        self.table.item(row, 2).setText(new_val)
        self.apply_row_color(row, code)

    def apply_row_color(self, row, code):
        excel = self.metrics[row]["desc"]
        transformed = self.mapping[code]["transformed"]

        if not transformed:
            color = QColor(255, 230, 230)
        elif transformed.strip() != excel.strip():
            color = QColor(255, 255, 200)
        else:
            color = QColor(230, 255, 230)

        for col in range(3):
            self.table.item(row, col).setBackground(color)

    def revalidate_all_rows(self):
        has_errors = False
        for row, m in enumerate(self.metrics):
            code = m["code"]
            excel = m["desc"]
            transformed = self.mapping[code]["transformed"]
            if not transformed or transformed.strip() != excel.strip():
                has_errors = True
            self.apply_row_color(row, code)
        self.btn_save.setEnabled(not has_errors)

    def on_save(self):
        mapping_file = f"config/metrics_mapping_{self.group_type}.py"
        try:
            new_mapping = {}
            for i in range(self.table.rowCount()):
                code = self.table.item(i, 0).text().strip()
                desc = self.table.item(i, 2).text().strip()
                if code and desc:
                    new_mapping[code] = desc

            text = "MAPPING = {\n"
            for k, v in new_mapping.items():
                text += f"    '{k}': '{v}',\n"
            text += "}\n"

            with open(mapping_file, "w", encoding="utf-8") as f:
                f.write(text)

            QMessageBox.information(
                self, "Сақталды", f"Mapping жаңартылды: {mapping_file}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Қате", f"Сақтау кезінде қате: {e}")
