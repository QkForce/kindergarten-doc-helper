from PySide6.QtWidgets import QMessageBox

from gui.steps.base_step import BaseStep
from gui.widgets.file_picker import FilePickerWidget
from gui.state import GeneratorState


class StepFileSelectOptions:
    def __init__(
        self,
        file_picker_label: str = "Шаблондық файл",
        file_picker_btn_text: str = "Файлды таңдау",
        file_picker_caption: str = "Шаблондық файлды таңдау",
        file_picker_dir: str = "",
        file_picker_filter: str = "DOCX Files (*.docx)",
        validation_error_msg: str = "Шаблондық файлды таңдаңыз.",
        state_file_attr_name: str = "temp_file_path",
    ):
        self.file_picker_label = file_picker_label
        self.file_picker_btn_text = file_picker_btn_text
        self.file_picker_caption = file_picker_caption
        self.file_picker_dir = file_picker_dir
        self.file_picker_filter = file_picker_filter
        self.validation_error_msg = validation_error_msg
        self.state_file_attr_name = state_file_attr_name


class StepFileSelect(BaseStep[GeneratorState]):
    def __init__(
        self, state: GeneratorState, options: StepFileSelectOptions, parent=None
    ):
        self.options = options
        super().__init__(state, parent=parent)

    def setup_ui(self):
        self.file_select_widget = FilePickerWidget(
            self.options.file_picker_label,
            self.options.file_picker_btn_text,
            self.options.file_picker_caption,
            self.options.file_picker_dir,
            self.options.file_picker_filter,
        )

        self.layout.addWidget(self.file_select_widget)
        self.layout.addStretch()

    def setup_state_machine(self):
        return

    def connect_signals(self):
        self.file_select_widget.fileSelected.connect(
            lambda selected_file: setattr(
                self.state, self.options.state_file_attr_name, selected_file
            )
        )

    def run_auto_load(self):
        return

    def validate_before_next(self):
        if not getattr(self.state, self.options.state_file_attr_name):
            QMessageBox.warning(self, "Ескерту", self.options.validation_error_msg)
            return False
        return True
