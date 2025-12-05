from openpyxl import load_workbook
from config.config import AGE_GROUP_DATA

METRIC_CODES = [
    code
    for metric_group_data in AGE_GROUP_DATA.values()
    for code in metric_group_data.keys()
]


def load_metrics_from_excel(file_path, sheet_name, min_row=14, max_row=38):
    workbook = load_workbook(filename=file_path)
    sheet = workbook[sheet_name]

    children_data = []
    for row in sheet.iter_rows(min_row=min_row, max_row=max_row, values_only=True):
        child = {
            "number": row[0],
            "name": row[1],
        }
        for index, metrics_key in enumerate(METRIC_CODES):
            if row[2 + index * 3] is not None:
                child[metrics_key] = 1
            elif row[2 + index * 3 + 1] is not None:
                child[metrics_key] = 2
            elif row[2 + index * 3 + 2] is not None:
                child[metrics_key] = 3
        children_data.append(child)
    return children_data
