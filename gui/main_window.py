from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from gui.pages.hub_page import HubPage
from gui.pages.generator_page import GeneratorPage
from gui.constants.strings import AppStrings
from gui.utils.window_utils import center_on_screen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. WINDOW
        self.setWindowTitle(AppStrings.APP_NAME)
        self.setMinimumSize(950, 650)
        center_on_screen(self)

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
        self.hub_page = HubPage()
        self.hub_page.generator_requested.connect(lambda: self.switch_page(1))
        self.hub_page.template_requested.connect(lambda: self.switch_page(2))
        self.hub_page.entry_requested.connect(lambda: self.switch_page(3))
        self.stack.addWidget(self.hub_page)

        # Index 1: GENERATOR FLOW
        self.generator_page = GeneratorPage(on_finish=lambda: self.switch_page(0))
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
