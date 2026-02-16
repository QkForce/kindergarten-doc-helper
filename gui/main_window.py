from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. WINDOW
        self.setWindowTitle("KinderDoc Helper")
        self.setMinimumSize(1000, 700)

        # 2. MAIN STACK
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # 3. PAGES
        self.init_pages()

    def init_pages(self):
        # Index 0: HUB PAGE
        self.hub_page = QWidget()
        self.stack.addWidget(self.hub_page)

        # Index 1: GENERATOR FLOW
        self.generator_page = QWidget()
        self.stack.addWidget(self.generator_page)

        # Index 2: TEMPLATE FILLER
        self.template_page = QWidget()
        self.stack.addWidget(self.template_page)

        # Index 3: SMART ENTRY
        self.entry_page = QWidget()
        self.stack.addWidget(self.entry_page)

        # First page - Hub
        self.stack.setCurrentIndex(0)

    def switch_page(self, index: int):
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)
