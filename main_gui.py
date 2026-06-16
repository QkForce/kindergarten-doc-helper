import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from gui.utils.style_utils import load_stylesheets

app = QApplication(sys.argv)


load_stylesheets(
    app,
    [
        "gui/resources/style/global.qss",
        "gui/resources/style/style.qss",
        "gui/resources/style/step1.qss",
    ],
)

window = MainWindow()
window.show()
sys.exit(app.exec())
