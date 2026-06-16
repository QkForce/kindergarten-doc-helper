from pathlib import Path
from functools import wraps

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QMessageBox

from gui.utils.style_utils import load_stylesheets


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


def init_test_page(qtbot, page_class, stylesheets: list, config, **kwargs):
    page = page_class(**kwargs)
    qtbot.addWidget(page)

    app = QApplication.instance() or QApplication([])
    load_stylesheets(app, stylesheets)
    page.setMinimumSize(config.window_min_width, config.window_min_height)

    page.show()
    qtbot.waitExposed(page)

    return page


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


def sync_worker(task_function, finished_slot, error_slot):
    try:
        print("\n[WORKER] Тапсырма орындалуда...")
        result = task_function()
        print("[WORKER] Тапсырма сәтті аяқталды!")
        QApplication.processEvents()
        finished_slot(result)
        QApplication.processEvents()
    except Exception as exc:
        print(f"\n❌ [CRITICAL WORKER ERROR]: {exc}")
        error_slot(str(exc))
        raise exc
