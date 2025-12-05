import os
from dotenv import load_dotenv
from config.metrics_schema import METRICS_SCHEMA

load_dotenv()

XLSX_FILE_PATH = os.getenv("XLSX_FILE_PATH")
XLSX_SHEET_NAME = os.getenv("XLSX_SHEET_NAME")
TEMPLATE_DOCX_PATH = os.getenv("TEMPLATE_DOCX_PATH")
OUTPUT_DOCX_PATH = os.getenv("OUTPUT_DOCX_PATH")
GROUP_TYPE = os.getenv("GROUP_TYPE", "ересек топ")
ROW_START = int(os.getenv("ROW_START", 14))
ROW_END = int(os.getenv("ROW_END", 38))

AGE_GROUP_DATA = METRICS_SCHEMA[GROUP_TYPE]
