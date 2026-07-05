_ENGLISH_ALPHABET = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
_KAZAKH_ALPHABET = (
    "АаӘәБбВвГгҒғДдЕеЁёЖжЗзИиЙйКкҚқЛлМмНнҢңОоӨөПпРрСсТтУуҰұҮүФфХхҺһЦц"
    "ЧчШшЩщЪъЫыІіЬьЭэЮюЯя"
)
_ALPHABET = _ENGLISH_ALPHABET + _KAZAKH_ALPHABET

_CHAR_WEIGHTS = {char: idx for idx, char in enumerate(_ALPHABET)}

_DEFAULT_DATE_SORT_KEY = (9999, 12, 31)


def get_sort_key(text: str) -> list:
    if not text:
        return []
    default_weight = len(_ALPHABET)
    return [_CHAR_WEIGHTS.get(char, default_weight) for char in text]


def get_date_sort_key(date_str: str) -> tuple:
    if not date_str:
        return _DEFAULT_DATE_SORT_KEY
    try:
        parts = date_str.split("-")
        if len(parts) == 3:
            year, month, day = map(int, parts)
            return (year, month, day)
        parts = date_str.split(".")
        if len(parts) == 3:
            day, month, year = map(int, parts)
            return (year, month, day)
        return _DEFAULT_DATE_SORT_KEY
    except ValueError:
        return _DEFAULT_DATE_SORT_KEY
