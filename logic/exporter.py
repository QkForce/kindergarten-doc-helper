from gui.state import ChecklistBaseState
from logic.docx_tools import create_children_grow_cards, fill_all_children_in_big_file
from logic.metrics_tools import prepare_all_children_grow_card_data
from logic.xlsx_tools import fill_assessment_table


class Exporter:
    def set_data(self, state: ChecklistBaseState, age_group_data, progress_callback):
        pass

    def export(self):
        pass


class DocxGenerateExporter(Exporter):
    def set_data(self, state: ChecklistBaseState, age_group_data, progress_callback):
        self.state = state
        self.age_group_data = age_group_data
        self.progress_callback = progress_callback
        self.all_children_data = prepare_all_children_grow_card_data(
            state.children_scores, age_group_data
        )

    def export(self):
        docx = create_children_grow_cards(
            self.state.temp_file_path,
            self.all_children_data,
            self.progress_callback,
        )
        return docx


class DocxFillExporter(Exporter):
    def set_data(self, state: ChecklistBaseState, age_group_data, progress_callback):
        self.state = state
        self.age_group_data = age_group_data
        self.progress_callback = progress_callback
        self.all_children_data = prepare_all_children_grow_card_data(
            state.children_scores, age_group_data
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
    def set_data(self, state: ChecklistBaseState, age_group_data, progress_callback):
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
        self.metrics_codes = [
            metric_code
            for metrics in age_group_data.values()
            for metric_code in metrics.keys()
        ]
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
