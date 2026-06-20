from PySide6.QtWidgets import QMessageBox

from gui.steps.base_step import BaseStep
from gui.widgets.file_picker import FilePickerWidget
from gui.state import GeneratorState


class StepGrowFormConfig(BaseStep[GeneratorState]):
    def setup_ui(self):
        self.grow_card_file_select_widget = FilePickerWidget(
            "Балалардың даму картасы файлы (.docx)",
            "Файлды таңдау",
            "Балалардың даму картасы файлын таңдаңыз",
            "",
            "Document Files (*.docx)",
        )
        self.temp_file_select_widget = FilePickerWidget(
            "Шаблондық файл",
            "Файлды таңдау",
            "Шаблондық файлды таңдау",
            "",
            "Document Files (*.docx)",
        )

        self.layout.addWidget(self.grow_card_file_select_widget)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.temp_file_select_widget)
        self.layout.addStretch()

    def setup_state_machine(self):
        return

    def connect_signals(self):
        self.grow_card_file_select_widget.fileSelected.connect(
            lambda selected_file: setattr(
                self.state, "grow_card_file_path", selected_file
            )
        )
        self.temp_file_select_widget.fileSelected.connect(
            lambda selected_file: setattr(self.state, "temp_file_path", selected_file)
        )

    def run_auto_load(self):
        return

    def validate_before_next(self):
        if not self.state.grow_card_file_path:
            QMessageBox.warning(
                self, "Ескерту", "Балалардың даму картасы файлын таңдаңыз."
            )
            return False
        if not self.state.temp_file_path:
            QMessageBox.warning(self, "Ескерту", "Шаблондық файлды таңдаңыз.")
            return False
        return True
