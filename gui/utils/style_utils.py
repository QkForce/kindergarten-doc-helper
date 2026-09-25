import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

from gui.constants.colors import AppColors


def get_resource_path(relative_path: str) -> Path:
    """
    EXE режимінде (sys._MEIPASS) және жай Python режимінде
    ресурстардың нақты абсолютті жолын қайтарады.
    """
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        # Скрипт ретінде іске қосылғанда жобаның негізгі папкасын табу
        base_path = Path(__file__).resolve().parent.parent.parent

    return base_path / relative_path


def read_stylesheet(file_path: str | Path):
    path = Path(file_path)
    with open(path, "r", encoding="utf-8") as f:
        style_data = f.read()

    for key, value in AppColors.__dict__.items():
        if not key.startswith("__") and isinstance(value, str):
            style_data = style_data.replace("@" + key, value)

    if "@" in style_data:
        print(f"⚠️ [STYLE WARNING]: Unreplaced color variables in {path.name}")

    return style_data


def load_stylesheets(target, qss_file_paths: list[str]):
    combined_style = ""
    loaded_count = 0

    for file_path in qss_file_paths:
        # Жолды уақытша папкаға немесе негізгі директорияға сілтеп түрлендіру:
        full_path = get_resource_path(file_path)

        if full_path.exists():
            combined_style += read_stylesheet(full_path) + "\n"
            loaded_count += 1
        else:
            print(f"⚠️ [STYLE WARNING]: Файл табылмады: {full_path.absolute()}")

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