_ENGLISH_ALPHABET = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
_KAZAKH_ALPHABET = (
    "АаӘәБбВвГгҒғДдЕеЁёЖжЗзИиЙйКкҚқЛлМмНнҢңОоӨөПпРрСсТтУуҰұҮүФфХхҺһЦц"
    "ЧчШшЩщЪъЫыІіЬьЭэЮюЯя"
)
_ALPHABET = _ENGLISH_ALPHABET + _KAZAKH_ALPHABET

_CHAR_WEIGHTS = {char: idx for idx, char in enumerate(_ALPHABET)}


def get_sort_key(text: str) -> list:
    if not text:
        return []
    default_weight = len(_ALPHABET)
    return [_CHAR_WEIGHTS.get(char, default_weight) for char in text]
