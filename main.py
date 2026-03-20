from logic.xlsx_tools import load_metrics_from_excel
from logic.metrics_tools import build_all_grow_cards
from logic.docx_tools import create_children_grow_cards
from config.config import (
    XLSX_FILE_PATH,
    AGE_GROUP_DATA,
    TEMPLATE_DOCX_PATH,
    OUTPUT_DOCX_PATH,
    XLSX_SHEET_NAME,
    ROW_START,
    ROW_END,
)


def print_process(fullname, current_index, total_children):
    print(f"Processing child: {fullname} ({current_index}/{total_children})")


if __name__ == "__main__":
    children_data = load_metrics_from_excel(
        XLSX_FILE_PATH,
        XLSX_SHEET_NAME,
        ROW_START,
        ROW_END,
    )
    all_children_grow_card_data = build_all_grow_cards(
        children_data, AGE_GROUP_DATA
    )
    merged_doc = create_children_grow_cards(
        TEMPLATE_DOCX_PATH, all_children_grow_card_data, print_process
    )
    merged_doc.save(OUTPUT_DOCX_PATH)
