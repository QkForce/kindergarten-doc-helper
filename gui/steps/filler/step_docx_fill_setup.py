from PySide6.QtWidgets import (
    QComboBox,
    QVBoxLayout,
    QMessageBox,
    QLabel,
)

from gui.steps.step_widget import StepWidget
from gui.widgets.file_picker import FilePickerWidget
from gui.state import FillerState
from gui.constants.strings import AppStrings


class StepDocxFillSetup(StepWidget[FillerState]):
    def setup_ui(self):
        # File selection widget
        self.file_select_widget = FilePickerWidget(
            "Шаблондық файл",
            "Файлды таңдау",
            "Шаблондық файлды таңдау",
            "",
            "Document Files (*.docx)",
        )

        # Control type selection label
        control_types_label = QLabel("Бақылау түрі:")
        control_types_label.setProperty("lbl-level", "lbl")

        # Control type selection combo box
        self.combo_control_types = QComboBox()
        control_types_label.setBuddy(self.combo_control_types)
        self.control_types = {
            1: "Бастапқы бақылау",
            2: "Аралық бақылау",
            3: "Қорытынды бақылау",
        }
        for key, display_text in self.control_types.items():
            self.combo_control_types.addItem(display_text, key)
        self.state.control_type = self.combo_control_types.currentData()

        # Layout setup
        layout = QVBoxLayout(self)
        layout.addWidget(self.file_select_widget)
        layout.addWidget(control_types_label)
        layout.addWidget(self.combo_control_types)
        layout.addStretch()

    def setup_state_machine(self):
        return

    def connect_signals(self):
        self.file_select_widget.fileSelected.connect(
            lambda selected_file: setattr(self.state, "temp_file_path", selected_file)
        )
        self.combo_control_types.currentIndexChanged.connect(
            lambda: setattr(
                self.state, "control_type", self.combo_control_types.currentData()
            )
        )

    def run_auto_load(self):
        return

    def validate_before_next(self):
        if not self.state.temp_file_path:
            QMessageBox.warning(self, "Ескерту", "Шаблондық файлды таңдаңыз.")
            return False
        if not self.state.control_type:
            QMessageBox.warning(self, "Ескерту", "Бақылау түрін таңдаңыз.")
            return False
        return True
