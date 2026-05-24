from pathlib import Path
from PySide6.QtWidgets import QApplication


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
