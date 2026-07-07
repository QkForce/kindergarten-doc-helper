from docx import Document

from PySide6.QtWidgets import QMessageBox

from gui.steps.base_loader_step import BaseLoaderStep, StepLoaderOptions
from gui.state import GrowFormState
from gui.steps.contents.sort_children_content import SortChildrenContent
from logic.grow_card_parser import GrowCardParser


class StepSortChildren(BaseLoaderStep[GrowFormState]):
    def __init__(self, state, parent=None):
        options = StepLoaderOptions(
            loading_title="Деректерді талдау",
            loading_desc="Балалардың даму картасын талдау және топтағы балалар тізімін шығару",
            empty_title="Балалар тізімі бос",
            empty_desc=(
                "Файлдағы балалар тізімі бос немесе талдау кезінде қате пайда болды. "
                "Өтінеміз, дұрыс файл таңдағаныңызды тексеріңіз."
            ),
            error_title="Файлды талдау кезіндегі қате",
            error_desc=(
                "Файлды оқу кезінде қате пайда болды: {} "
                "Өтінеміз, дұрыс файл таңдағаныңызды тексеріңіз."
            ),
        )
        content_widget = SortChildrenContent()
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
        data = self.content_widget.getData()
        self.state.students_cards = data["students_cards"]
        self.state.academic_year = data["academic_year"]
        self.state.group_name = data["group_name"]
        if not self.state.students_cards:
            QMessageBox.critical(
                self,
                "Деректер бүтіндігінің бұзылуы",
                "Топтағы балалар тізімі бос. Өтінеміз, дұрыс файл таңдағаныңызды тексеріңіз.",
            )
            return False
        if not self.state.academic_year:
            QMessageBox.critical(
                self,
                "Деректер бүтіндігінің бұзылуы",
                "Оқу жылы анықталмады. Өтінеміз, дұрыс файл таңдағаныңызды тексеріңіз.",
            )
            return False
        if not self.state.group_name:
            QMessageBox.critical(
                self,
                "Деректер бүтіндігінің бұзылуы",
                "Топ атауы анықталмады. Өтінеміз, дұрыс файл таңдағаныңызды тексеріңіз.",
            )
            return False
        return True

    def is_result_empty(self, result):
        return not (result and len(result.get("students_cards", [])) > 0)

    def loaded(self, result: dict):
        self.state.academic_year = result["academic_year"]
        self.state.group_name = result["group_name"]
        self.state.students_cards = result["students_cards"]

        self.content_widget.applyData(**result)

    def load_failed(self, err):
        # It isn't necessary to show the error message here,
        # because the BaseLoaderStep already shows it in the error state.
        return
