import sys
from PySide6.QtWidgets import QApplication
from gui.constants.colors import AppColors
from gui.main_window import MainWindow

app = QApplication(sys.argv)


def load_stylesheet(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    for key, value in AppColors.__dict__.items():
        if not key.startswith("__") and isinstance(value, str):
            content = content.replace("@" + key, value)

    if "@" in content:
        print(f"Warning: Unreplaced color variables in {file_path}")

    return content


app.setStyleSheet(app.styleSheet() + load_stylesheet("gui/resources/style/global.qss"))
app.setStyleSheet(app.styleSheet() + load_stylesheet("gui/resources/style/style.qss"))
app.setStyleSheet(app.styleSheet() + load_stylesheet("gui/resources/style/step1.qss"))

window = MainWindow()
window.show()
sys.exit(app.exec())
