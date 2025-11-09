import os
from dotenv import load_dotenv
from config import metrics_mapping_adult


load_dotenv()


XLSX_FILE_PATH = os.getenv("XLSX_FILE_PATH")
TEMPLATE_DOCX_PATH = os.getenv("TEMPLATE_DOCX_PATH")
OUTPUT_DOCX_PATH = os.getenv("OUTPUT_DOCX_PATH")
GROUP_TYPE = os.getenv("GROUP_TYPE", "ересек топ")
ROW_START = int(os.getenv("ROW_START", 14))
ROW_END = int(os.getenv("ROW_END", 38))

GROUPS = {
    "ересек топ": {
        "sheet_name": "ересек топ",
        "row_start": ROW_START,
        "row_end": ROW_END,
        "metrics_mapping": metrics_mapping_adult.MAPPING,
    },
    "мектепалды топ": {
        "sheet_name": "мектепалды топ",
        "row_start": ROW_START,
        "row_end": ROW_END,
        "metrics_mapping": metrics_mapping_adult.MAPPING,
    },
}

GROUP_CONF = GROUPS[GROUP_TYPE]
