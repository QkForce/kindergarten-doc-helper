from PySide6.QtWidgets import QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from gui.pages.hub_page import HubPage
from gui.pages.generator_page import GeneratorPage
from gui.pages.smart_entry_page import SmartEntryPage
from gui.pages.filler_page import FillerPage
from gui.constants.strings import AppStrings
from gui.utils.window_utils import center_on_screen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # WINDOW
        self.setWindowTitle(AppStrings.APP_NAME)
        self.setMinimumSize(950, 650)
        center_on_screen(self)

        # MAIN STACK
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        # SHOW HUB
        self.show_hub()

    def show_hub(self):
        self._clear_stack()

        hub = HubPage()
        hub.generator_requested.connect(self.show_generator)
        hub.template_requested.connect(self.show_filler)
        hub.entry_requested.connect(self.show_smart_entry)

        self.stack.addWidget(hub)
        self.stack.setCurrentWidget(hub)

    def show_generator(self):
        page = GeneratorPage(on_finish=self.show_hub)
        self._add_and_switch(page)

    def show_filler(self):
        page = FillerPage(on_finish=self.show_hub)
        self._add_and_switch(page)

    def show_smart_entry(self):
        page = SmartEntryPage(on_finish=self.show_hub)
        self._add_and_switch(page)

    def _add_and_switch(self, widget):
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

    def _clear_stack(self):
        while self.stack.count() > 0:
            widget = self.stack.widget(0)
            self.stack.removeWidget(widget)
            widget.deleteLater()
