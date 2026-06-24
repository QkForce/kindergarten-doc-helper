from docx import Document

from PySide6.QtWidgets import (
    QListWidget,
    QAbstractItemView,
    QListWidgetItem,
)

from gui.steps.base_loader_step import BaseLoaderStep, StepLoaderOptions
from gui.state import GrowFormState
from logic.grow_card_parser import GrowCardParser


class StepSortChildren(BaseLoaderStep[GrowFormState]):
    def __init__(self, state, parent=None):
        options = StepLoaderOptions(
            loading_title="",
            loading_desc="",
            empty_title="",
            empty_desc="",
            error_title="",
            error_desc="",
        )
        content_widget = QListWidget()
        content_widget.setDragEnabled(True)
        content_widget.setAcceptDrops(True)
        content_widget.setDropIndicatorShown(True)
        content_widget.setDragDropMode(QAbstractItemView.InternalMove)
        super().__init__(state, options, content_widget, parent)

    def connect_signals(self):
        return

    def load_auto(self):
        self.grow_card_docx = Document(self.state.grow_card_file_path)
        parser = GrowCardParser(self.grow_card_docx)
        academic_year = parser.parse_academic_year()
        group_name = parser.parse_group_name()
        students_cards = parser.parse()
        return {
            "students_cards": students_cards,
            "academic_year": academic_year,
            "group_name": group_name,
        }

    def validate_before_next(self):
        sorted_cards = []
        for i in range(self.content_widget.count()):
            item = self.content_widget.item(i)
            child_data = item.data(100)
            sorted_cards.append(child_data)
        self.state.students_cards = sorted_cards
        return True

    def is_result_empty(self, result):
        return not (result and len(result.get("students_cards", [])) > 0)

    def loaded(self, result: dict):
        self.state.academic_year = result["academic_year"]
        self.state.group_name = result["group_name"]
        self.state.students_cards = result["students_cards"]

        self.content_widget.clear()
        for child in result["students_cards"]:
            fullname = child.get("fullname", "Белгісіз бала")
            item = QListWidgetItem(fullname)
            item.setData(100, child)
            self.content_widget.addItem(item)

    def load_failed(self, err):
        return
