from typing import List


class ScoresLoader:
    def __init__(self, sheet):
        self.sheet = sheet

    def load_manual(
        self,
        start_row: int,
        end_row: int,
        name_col: int,
        metrics_start_col: int,
        metric_codes: List[int],
    ):
        name_col -= 1
        metrics_start_col -= 1
        children_rates = []
        for row in self.sheet.iter_rows(
            min_row=start_row, max_row=end_row, values_only=True
        ):
            item = {"name": row[name_col]}
            for col, code in enumerate(metric_codes):
                if row[metrics_start_col + col * 3] is not None:
                    item[code] = 1
                elif row[metrics_start_col + col * 3 + 1] is not None:
                    item[code] = 2
                elif row[metrics_start_col + col * 3 + 2] is not None:
                    item[code] = 3
                else:
                    item[code] = 0
            children_rates.append(item)
        return children_rates
