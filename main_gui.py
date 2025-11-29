import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

app = QApplication(sys.argv)

with open("gui/resources/style/global.qss", "r", encoding="utf-8") as f:
    app.setStyleSheet(app.styleSheet() + f.read())
with open("gui/resources/style/style.qss", "r", encoding="utf-8") as f:
    app.setStyleSheet(app.styleSheet() + f.read())
with open("gui/resources/style/step1.qss", "r", encoding="utf-8") as f:
    app.setStyleSheet(app.styleSheet() + f.read())

window = MainWindow()
window.show()
sys.exit(app.exec())
