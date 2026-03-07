from gui.state import ChecklistBaseState
from logic.xlsx_tools import fill_assessment_table


class Exporter:
    def set_data(self, state: ChecklistBaseState, age_group_data, progress_callback):
        pass

    def export(self):
        pass


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
