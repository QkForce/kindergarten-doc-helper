from pathlib import Path
from functools import wraps

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QMessageBox

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


def mock_ui_dialogs(test_func):
    @wraps(test_func)
    def wrapper(*args, **kwargs):
        monkeypatch = kwargs.get("monkeypatch")
        if not monkeypatch:
            for arg in args:
                if type(arg).__name__ == "MonkeyPatch":
                    monkeypatch = arg
                    break

        if monkeypatch:
            monkeypatch.setattr(
                QMessageBox, "information", lambda *args, **kwargs: None
            )
            monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: None)
            monkeypatch.setattr(QMessageBox, "critical", lambda *args, **kwargs: None)

        return test_func(*args, **kwargs)

    return wrapper


def click_list_item(list_widget, idx):
    item = list_widget.item(idx)
    list_widget.scrollToItem(item)
    QApplication.processEvents()
    item_rect = list_widget.visualItemRect(item)
    QTest.mouseClick(list_widget.viewport(), Qt.LeftButton, pos=item_rect.center())
    QApplication.processEvents()
