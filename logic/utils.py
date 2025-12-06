import re
import string


def sentences_equal(a: str, b: str) -> bool:
    a = a.lower()
    b = b.lower()

    punct = string.punctuation + "«»„“”"
    table = str.maketrans("", "", punct)
    a = a.translate(table)
    b = b.translate(table)

    a = re.sub(r"\s+", " ", a).strip()
    b = re.sub(r"\s+", " ", b).strip()

    return a == b
