from openpyxl.worksheet.worksheet import Worksheet


def find_table_origin(sheet, marker="№"):
    ref_row, ref_col = None, None
    for r in range(1, 31):
        for c in range(1, 11):
            val = sheet.cell(row=r, column=c).value
            if val and str(val).strip() == marker:
                ref_row, ref_col = r, c
                break
        if ref_row:
            break

    if not ref_row:
        return 4, 1
    start_row = ref_row
    for r in range(ref_row - 1, 1, -1):
        if sheet.cell(row=r, column=ref_col).border.top.style is not None:
            start_row = r
            return start_row, ref_col

    return start_row, ref_col


def find_student_list_start_row(sheet: Worksheet, start_row, start_col):
    for r in range(start_row, start_row + 20):
        val = sheet.cell(row=r, column=start_col).value
        if val is not None and str(val).strip() == "1":
            return r
    return start_row + 10


def find_student_name_col_index(sheet: Worksheet, header_row=12, marker="баланың аты"):
    for col in range(1, 10):
        val = sheet.cell(row=header_row, column=col).value
        if val and marker in str(val).lower():
            return col
    return 2


def find_footer_row_index(sheet: Worksheet, marker="барлығы"):
    for row in range(1, 200):
        val = sheet.cell(row=row, column=1).value
        if val and marker in str(val).lower():
            return row
    return None


def find_last_data_col_index(sheet: Worksheet, reference_row):
    curr_col = 2
    while True:
        if sheet.cell(row=reference_row, column=curr_col + 1).value is None:
            break
        curr_col += 1
    return curr_col
