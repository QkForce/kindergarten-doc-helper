from typing import TypeVar

from PySide6.QtWidgets import QLabel, QComboBox, QMessageBox, QSizePolicy

from gui.steps.base_step import BaseStep
from gui.widgets.file_picker import FilePickerWidget
from gui.state import ChecklistBaseState
from gui.constants.strings import AppStrings, AGE_GROUPS
from logic.xlsx_tools import get_sheet_names


T = TypeVar("T", bound=ChecklistBaseState)


class StepFileSelect(BaseStep[T]):
    def setup_ui(self):
        # Excel файлды таңдау
        self.file_select_widget = FilePickerWidget("Мониторинг файлы")
        self.file_select_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )

        # Sheet таңдау
        self.combo_sheet = QComboBox()
        self.combo_sheet.setEnabled(False)

        sheet_label = QLabel("Кесте (sheet) атауы:")
        sheet_label.setBuddy(self.combo_sheet)
        sheet_label.setProperty("lbl-level", "lbl")

        # Топ түрін таңдау
        self.combo_group = QComboBox()
        for key, display_text in AGE_GROUPS.items():
            self.combo_group.addItem(display_text, key)

        group_type_label = QLabel("Топ түрі:")
        group_type_label.setBuddy(self.combo_group)
        group_type_label.setProperty("lbl-level", "lbl")

        # ---- Layout ----
        self.layout.addWidget(self.file_select_widget)
        self.layout.addSpacing(10)

        self.layout.addWidget(sheet_label)
        self.layout.addWidget(self.combo_sheet)
        self.layout.addSpacing(10)

        self.layout.addWidget(group_type_label)
        self.layout.addWidget(self.combo_group)
        self.layout.addStretch()

    def setup_state_machine(self):
        return

    def connect_signals(self):
        self.file_select_widget.fileSelected.connect(self.select_excel_file)

    def select_excel_file(self, file_path):
        try:
            self.state.file_path = file_path
            self.combo_sheet.clear()
            self.combo_sheet.addItems(get_sheet_names(file_path))
            self.combo_sheet.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Қате", f"Файлды оқу кезінде қате:\n{e}")
            self.combo_sheet.setEnabled(False)

    def validate_before_next(self):
        if not self.state.file_path:
            QMessageBox.warning(self, "Ескерту", "Excel файлын таңдаңыз.")
            return False

        if not self.combo_sheet.currentText():
            QMessageBox.warning(self, "Ескерту", "Кесте (sheet) атауын таңдаңыз.")
            return False

        self.state.sheet_name = self.combo_sheet.currentText()
        self.state.age_group = self.combo_group.currentData()

        return True
