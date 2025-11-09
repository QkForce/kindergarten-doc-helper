from logic.xlsx_tools import load_metrics_from_excel
from logic.metrics_tools import prepare_all_children_grow_card_data
from logic.docx_tools import create_children_grow_cards
from config.config import (
    XLSX_FILE_PATH,
    GROUP_CONF,
    TEMPLATE_DOCX_PATH,
    OUTPUT_DOCX_PATH,
)


if __name__ == "__main__":
    children_data = load_metrics_from_excel(
        XLSX_FILE_PATH,
        GROUP_CONF["sheet_name"],
        GROUP_CONF["row_start"],
        GROUP_CONF["row_end"],
    )
    all_children_grow_card_data = prepare_all_children_grow_card_data(children_data)
    create_children_grow_cards(
        TEMPLATE_DOCX_PATH, all_children_grow_card_data, OUTPUT_DOCX_PATH
    )
