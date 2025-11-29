from typing import Tuple, Optional, List
import re
from difflib import SequenceMatcher


def normalize_text(s: Optional[str]) -> str:
    if s is None:
        return ""
    s = str(s).lower()
    s = re.sub(r"[^\w\-\sңғүқөәіһёүңәөҢҒҮҚӘІҺ]", " ", s, flags=re.UNICODE)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def fuzzy_ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def is_empty(sheet, row, col):
    value = sheet.cell(row=row, column=col).value
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def normalize_code_text(v):
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip().replace(" ", "").upper()
    return str(v).strip().upper()


def is_metric_code(value: str) -> bool:
    if not value:
        return False
    txt = normalize_code_text(value)
    pattern = r"^[0-9]+-[ФКТШӘ]\.[0-9]+$"
    return re.match(pattern, txt) is not None


def find_next_nonempty_row(sheet, start_row, col):
    for r in range(start_row + 1, sheet.max_row + 1):
        if not is_empty(sheet, r, col):
            return r
    return None
