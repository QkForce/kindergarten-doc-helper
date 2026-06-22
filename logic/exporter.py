from docx import Document
from openpyxl import load_workbook

from gui.state import ChecklistBaseState, GrowFormState
from logic.docx_tools import (
    create_children_grow_cards,
    fill_all_children_in_big_file,
)
from logic.grow_card_builder import GrowCardBuilder
from logic.grow_card_parser import GrowCardParser
from logic.metrics_tools import build_all_grow_cards
from logic.xlsx_tools import (
    fill_assessment_table,
    get_table_boundaries,
    apply_complex_monitoring_borders,
    apply_monitoring_typography,
    apply_monitoring_number_rounding,
    apply_monitoring_formula_fixing,
    remove_empty_rows_and_cols,
)


class ExportResult:
    def __init__(self, data, errors=None):
        self.data = data
        self.errors = errors or []
        self.is_success = len(self.errors) == 0


class Exporter:
    def set_data(self, state: ChecklistBaseState, progress_callback):
        pass

    def export(self) -> ExportResult:
        pass


class DocxGenerateExporter(Exporter):
    def set_data(self, state: ChecklistBaseState, progress_callback):
        self.state = state
        self.progress_callback = progress_callback
        self.all_children_data = build_all_grow_cards(
            state.children_scores, state.age_group_data
        )

    def export(self) -> ExportResult:
        docx = create_children_grow_cards(
            self.state.temp_file_path,
            self.all_children_data,
            self.progress_callback,
        )
        return ExportResult(docx)


class DocxFillExporter(Exporter):
    def set_data(self, state: ChecklistBaseState, progress_callback):
        self.state = state
        self.progress_callback = progress_callback
        self.all_children_data = build_all_grow_cards(
            state.children_scores, state.age_group_data
        )

    def export(self) -> ExportResult:
        docx, missing_children = fill_all_children_in_big_file(
            self.state.temp_file_path,
            self.all_children_data,
            self.state.control_type,
            self.progress_callback,
        )
        return ExportResult(docx, missing_children)


class SmartEntryExporter(Exporter):
    def set_data(self, state: ChecklistBaseState, progress_callback):
        self.children_data = [
            {
                "name": name,
                **{
                    met["code"]: met["score"]
                    for dom in state.children_scores[name].values()
                    for sub in dom["subjects"].values()
                    for met in sub["metrics"].values()
                },
            }
            for name in state.original_children_order
        ]
        self.metrics_codes = state.metric_codes
        self.state = state
        self.progress_callback = progress_callback

    def export(self) -> ExportResult:
        workbook = fill_assessment_table(
            file_path=self.state.file_path,
            sheet_name=self.state.sheet_name,
            start_row=self.state.children_start_row,
            name_col=self.state.children_col,
            metrics_col=self.state.metric_start_col,
            metrics_codes=self.metrics_codes,
            children_data=self.children_data,
            progress_callback=self.progress_callback,
        )
        return ExportResult(workbook)


class MonFormExporter:
    def set_data(self, state: ChecklistBaseState, progress_callback):
        self.state = state
        self.action_index = 0
        active_actions = [a for a in self.state.actions.values() if a]
        self.total_actions = 2 + len(active_actions)  # load + detect + actions
        self.progress_callback = progress_callback

    def progress(self, label: str):
        self.action_index += 1
        self.progress_callback(label, self.action_index, self.total_actions)

    def export(self) -> ExportResult:
        self.progress("Файлды оқу...")
        workbook = load_workbook(
            filename=self.state.file_path,
            read_only=False,
        )
        sheet = workbook[self.state.sheet_name]

        self.progress("Құрылымын анықтау...")
        b = get_table_boundaries(sheet)

        if self.state.actions["fix_borders"]:
            self.progress("Жиектерді сызу...")
            apply_complex_monitoring_borders(sheet, **b)
        if self.state.actions["fix_typography"]:
            self.progress("Қаріптерді реттеу...")
            apply_monitoring_typography(sheet, **b)
        if self.state.actions["round_numbers"]:
            self.progress("Сандарды бүтіндеу...")
            apply_monitoring_number_rounding(sheet, **b)
        if self.state.actions["sync_formulas_with_student_count"]:
            self.progress("Формулаларды бала санына сәйкестендіру...")
            apply_monitoring_formula_fixing(sheet, **b)
        if self.state.actions["remove_empty_spaces"]:
            self.progress("Бос жолдар мен бағандарды жою...")
            remove_empty_rows_and_cols(sheet, **b)

        return ExportResult(workbook)


class GrowFormExporter(Exporter):
    def set_data(self, state: GrowFormState, progress_callback):
        self.state = state
        self.progress_callback = progress_callback
        self.action_index = 0
        self.total_actions = 1

    def progress(self, label: str):
        self.action_index += 1
        self.progress_callback(label, self.action_index, self.total_actions)

    def export(self) -> ExportResult:
        # self.progress("Балалардың даму картасы файлы оқылуда...")
        # grow_card_docx = Document(self.state.grow_card_file_path)

        # self.progress("Үлгі файлы оқылуда...")
        # temp_docx = Document(self.state.temp_file_path)

        grow_card_parser = GrowCardParser(self.state.grow_card_file_path)
        academic_year = grow_card_parser.parse_academic_year()
        students_cards = grow_card_parser.parse()

        grow_card_builder = GrowCardBuilder(self.state.temp_file_path)
        docx = grow_card_builder.build(students_cards, academic_year)
        self.progress("Балалардың даму картасы файлы оқылуда...")
        return ExportResult(docx)
