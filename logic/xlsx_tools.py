from time import sleep
from openpyxl import load_workbook
from config.config import AGE_GROUP_DATA

METRIC_CODES = [
    code
    for metric_group_data in AGE_GROUP_DATA.values()
    for code in metric_group_data.keys()
]


def get_sheet_names(file_path: str):
    workbook = load_workbook(file_path, read_only=True)
    try:
        return workbook.sheetnames
    finally:
        workbook.close()


def load_metrics_from_excel(file_path, sheet_name, min_row=14, max_row=38):
    workbook = load_workbook(filename=file_path, read_only=False)
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


def fill_assessment_table(
    file_path: str,
    sheet_name: str,
    start_row: int,
    name_col: int,
    metrics_col: int,
    metrics_codes: list,
    children_data: list,
    progress_callback=callable(lambda label, current_index, total_children: None),
):
    """
    children_data: { 'name': str, 'metric_code': score (1, 2, or 3) }
    """
    progress_callback("Loading the workbook", 0, 0)
    workbook = load_workbook(filename=file_path, read_only=False)
    sheet = workbook[sheet_name]
    current_row = start_row
    # metrics_col = name_col + 1
    for child in children_data:
        sheet.cell(row=current_row, column=name_col, value=child["name"])
        for metric_index, metric_code in enumerate(metrics_codes):
            score = child.get(metric_code)
            base_col = metrics_col + metric_index * 3

            # Clear previous values
            for offset in range(3):
                sheet.cell(row=current_row, column=base_col + offset).value = None

            # Set new value
            if score == 1:
                sheet.cell(row=current_row, column=base_col, value=1)
            elif score == 2:
                sheet.cell(row=current_row, column=base_col + 1, value=1)
            elif score == 3:
                sheet.cell(row=current_row, column=base_col + 2, value=1)
        progress_callback(
            child["name"], current_row - start_row + 1, len(children_data)
        )
        current_row += 1
        sleep(0.01)  # Simulate processing time
    return workbook
