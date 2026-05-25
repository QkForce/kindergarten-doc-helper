from pathlib import Path
from PySide6.QtWidgets import QApplication

from gui.constants.colors import AppColors


def mock_file_dialog(file_path):
    if isinstance(file_path, Path):
        ext = file_path.suffix.lstrip(".")
    else:
        ext = str(file_path).split(".")[-1] if "." in str(file_path) else ""
    return lambda *args, **kwargs: (str(file_path), ext)


def wait_until_visible(widget_attr_fn):
    def check_visibility():
        QApplication.processEvents()
        return widget_attr_fn()

    return check_visibility


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
