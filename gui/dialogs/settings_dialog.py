from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
)


class SettingsDialog(QDialog):
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Баптаулар")
        self.setMinimumSize(700, 500)

        left_bar_frame = QFrame()
        left_bar_frame.setFixedWidth(120)
        left_bar_layout = QVBoxLayout(left_bar_frame)

        body_frame = QFrame()
        body_layout = QVBoxLayout(body_frame)

        layout = QVBoxLayout(self)
        layout.addWidget(left_bar_frame)
        layout.addWidget(body_frame)

    def get_data(self):
        return {"export_path": self.path_input.text()}
