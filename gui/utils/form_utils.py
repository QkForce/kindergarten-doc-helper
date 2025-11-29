from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QSpinBox,
)


def create_vertical_field(label_text):
    v_layout = QVBoxLayout()
    label = QLabel(label_text)
    line_edit = QSpinBox()
    line_edit.setMinimumHeight(30)

    v_layout.addWidget(label)
    v_layout.addWidget(line_edit)

    return v_layout, line_edit
