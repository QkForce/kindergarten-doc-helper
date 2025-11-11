import os
from dotenv import load_dotenv
from config import (
    metrics_mapping_early_age,
    metrics_mapping_junior,
    metrics_mapping_middle,
    metrics_mapping_senior,
    metrics_mapping_preschool,
    metrics_groups_early_age,
    metrics_groups_junior,
    metrics_groups_middle,
    metrics_groups_senior,
    metrics_groups_preschool,
)


load_dotenv()


XLSX_FILE_PATH = os.getenv("XLSX_FILE_PATH")
XLSX_SHEET_NAME = os.getenv("XLSX_SHEET_NAME")
TEMPLATE_DOCX_PATH = os.getenv("TEMPLATE_DOCX_PATH")
OUTPUT_DOCX_PATH = os.getenv("OUTPUT_DOCX_PATH")
GROUP_TYPE = os.getenv("GROUP_TYPE", "ересек топ")
ROW_START = int(os.getenv("ROW_START", 14))
ROW_END = int(os.getenv("ROW_END", 38))

GROUPS = {
    "ерте жас тобы": {
        "sheet_name": XLSX_SHEET_NAME or "ерте жас тобы",
        "row_start": ROW_START,
        "row_end": ROW_END,
        "metrics_mapping": metrics_mapping_early_age.MAPPING,
        "metrics_groups": metrics_groups_early_age.METRICS_GROUPS,
    },
    "кіші топ": {
        "sheet_name": XLSX_SHEET_NAME or "кіші топ",
        "row_start": ROW_START,
        "row_end": ROW_END,
        "metrics_mapping": metrics_mapping_junior.MAPPING,
        "metrics_groups": metrics_groups_junior.METRICS_GROUPS,
    },
    "ортаңғы топ": {
        "sheet_name": XLSX_SHEET_NAME or "ортаңғы топ",
        "row_start": ROW_START,
        "row_end": ROW_END,
        "metrics_mapping": metrics_mapping_middle.MAPPING,
        "metrics_groups": metrics_groups_middle.METRICS_GROUPS,
    },
    "ересек топ": {
        "sheet_name": XLSX_SHEET_NAME or "ересек топ",
        "row_start": ROW_START,
        "row_end": ROW_END,
        "metrics_mapping": metrics_mapping_senior.MAPPING,
        "metrics_groups": metrics_groups_senior.METRICS_GROUPS,
    },
    "мектепалды тобы": {
        "sheet_name": XLSX_SHEET_NAME or "мектепалды тобы",
        "row_start": ROW_START,
        "row_end": ROW_END,
        "metrics_mapping": metrics_mapping_preschool.MAPPING,
        "metrics_groups": metrics_groups_preschool.METRICS_GROUPS,
    },
}

MARKERS_BY_TYPE = {
    "physical": "physical-1",
    "communicative": "communicative-1",
    "cognitive": "cognitive-1",
    "creativity": "creativity-1",
    "social": "social-1",
}

GROUP_CONF = GROUPS[GROUP_TYPE]
