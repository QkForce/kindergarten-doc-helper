from pathlib import Path

from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

from gui.constants.colors import AppColors


def read_stylesheet(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        style_data = f.read()

    for key, value in AppColors.__dict__.items():
        if not key.startswith("__") and isinstance(value, str):
            style_data = style_data.replace("@" + key, value)

    if "@" in style_data:
        print(f"⚠️ [STYLE WARNING]: Unreplaced color variables in {file_path}")

    return style_data


def load_stylesheets(target, qss_file_paths: list[str]):
    combined_style = ""
    loaded_count = 0

    for file_path in qss_file_paths:
        path = Path(file_path)
        if path.exists():
            combined_style += read_stylesheet(file_path) + "\n"
            loaded_count += 1
        else:
            print(f"⚠️ [STYLE WARNING]: Файл табылмады: {path.absolute()}")

    if combined_style and loaded_count == len(qss_file_paths):
        target.setStyleSheet(combined_style)
        QApplication.processEvents()
        return True
    return False


def apply_shadow(
    widget,
    color: QColor = QColor(0, 0, 0, 20),
    blur_radius: int = 25,
    offset_x: int = 0,
    offset_y: int = 8,
):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur_radius)
    shadow.setXOffset(offset_x)
    shadow.setYOffset(offset_y)
    shadow.setColor(color)
    widget.setGraphicsEffect(shadow)
