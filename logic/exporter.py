from gui.state import ChecklistBaseState
from logic.docx_tools import create_children_grow_cards, fill_all_children_in_big_file
from logic.metrics_tools import build_all_grow_cards
from logic.xlsx_tools import fill_assessment_table
from logic.config_tools import get_all_metric_codes


class Exporter:
    def set_data(self, state: ChecklistBaseState, progress_callback):
        pass

    def export(self):
        pass


class DocxGenerateExporter(Exporter):
    def set_data(self, state: ChecklistBaseState, progress_callback):
        self.state = state
        self.age_group_data = state.age_group_data
        self.progress_callback = progress_callback
        self.all_children_data = build_all_grow_cards(
            state.children_scores, state.age_group_data
        )

    def export(self):
        docx = create_children_grow_cards(
            self.state.temp_file_path,
            self.all_children_data,
            self.progress_callback,
        )
        return docx


class DocxFillExporter(Exporter):
    def set_data(self, state: ChecklistBaseState, progress_callback):
        self.state = state
        self.age_group_data = state.age_group_data
        self.progress_callback = progress_callback
        self.all_children_data = build_all_grow_cards(
            state.children_scores, state.age_group_data
        )

    def export(self):
        docx = fill_all_children_in_big_file(
            self.state.temp_file_path,
            self.all_children_data,
            self.state.control_type,
            self.progress_callback,
        )
        return docx


class SmartEntryExporter(Exporter):
    def set_data(self, state: ChecklistBaseState, progress_callback):
        self.children_data = [
            {
                "name": name,
                **{
                    metric_code: score
                    for subjects in scores.values()
                    for metrics in subjects.values()
                    for metric_code, score in metrics.items()
                },
            }
            for name, scores in state.children_scores.items()
        ]
        self.metrics_codes = get_all_metric_codes(state.age_group)
        self.state = state
        self.progress_callback = progress_callback

    def export(self):
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
        return workbook
