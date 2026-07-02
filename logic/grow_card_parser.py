import re
from collections import Counter

from docx import Document
from docx.document import Document as _Document
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from docx.oxml import CT_P, CT_Tbl


class GrowCardParser:
    def __init__(self, source):
        if isinstance(source, _Document):
            self.doc = source
        else:
            # If it gets str or BytesIO, python-docx will read and open it
            self.doc = Document(source)

    def iter_block_items(self, parent):
        if isinstance(parent, _Document):
            parent_elm = parent.element.body
        elif isinstance(parent, _Cell):
            parent_elm = parent._tc
        else:
            raise ValueError("Қате аталық элемент түрі")

        for child in parent_elm.iterchildren():
            if isinstance(child, CT_P):
                yield Paragraph(child, parent)
            elif isinstance(child, CT_Tbl):
                yield Table(child, parent)

    def parse_academic_year(self) -> str:
        for block in self.iter_block_items(self.doc):
            if not isinstance(block, Paragraph):
                continue
            text = block.text.strip()
            match = re.search(
                r"(\d{4})\s*[\-\–\—]\s*(\d{4})\s*оқу\s+жылына\s+арналған",
                text,
                re.IGNORECASE,
            )
            if match:
                start_year = match.group(1)
                end_year = match.group(2)
                return f"{start_year} – {end_year} оқу жылына арналған"

        raise ValueError(
            "Қате: Құжаттан 'XXXX – XXXX оқу жылына арналған' үлгісіне сәйкес "
            "ішкі жол табылмады!"
        )

    def parse_group_name(self) -> str:
        group_counter = Counter()
        stop_words = ["санаторлық", "топтарымен", "бөбекжай", "балабақшасы"]

        # Search and collect group names by template
        for block in self.iter_block_items(self.doc):
            if not isinstance(block, Paragraph):
                continue
            text = block.text.strip()
            if not text:
                continue
            matches = re.findall(r"([«\"'][^»\"']+[»\"']\s+\w+\s+\w+)", text)
            for match in matches:
                cleaned_match = self._clean_spaces(match)
                cleaned_match = re.sub(
                    r"^[«\"']([^»\"']+)[»\"']", r"«\1»", cleaned_match
                )
                if any(stop in cleaned_match.lower() for stop in stop_words):
                    continue
                group_counter[cleaned_match] += 1

        if not group_counter:
            raise ValueError(
                "Қате: Құжаттан топ атауы «...»\s+\w+\s+\w+ үлгісу бойынша табылмады!"
            )

        most_common = group_counter.most_common()
        if len(most_common) == 1 or most_common[0][1] > most_common[1][1]:
            return most_common[0][0]
        raise ValueError(
            "Қате: Топ атауын нақты анықтау мүмкін емес! "
            f"Бірдей жиілікте бірнеше нұсқа бар: {most_common}"
        )

    def parse(self) -> list[dict]:
        students_cards = []
        index = 0
        fullname, birth_date = "", ""

        for block in self.iter_block_items(self.doc):
            if isinstance(block, Paragraph):
                text = block.text.strip()
                if not text:
                    continue

                text_lower = text.lower()

                if "баланың т.а.ә" in text_lower or "т.а.ә" in text_lower:
                    keyword = (
                        "Т.А.Ә"
                        if "Т.А.Ә" in text
                        else ("т.а.ә" if "т.а.ә" in text else "Т.А.Ә")
                    )
                    fullname = self._clean_meta_value(text, keyword)
                elif "туған жылы" in text_lower or "күні" in text_lower:
                    keyword = "күні" if "күні" in text_lower else "жылы"
                    clean_kw = (
                        "күні"
                        if "күні" in text
                        else ("Күні" if "Күні" in text else "жылы")
                    )
                    raw_value = self._clean_meta_value(text, clean_kw)
                    birth_date = self._extract_birth_date(raw_value)

            elif isinstance(block, Table):
                if not block.rows or len(block.rows[0].cells) == 0:
                    continue

                if "Құзыреттіліктер" not in block.cell(0, 0).text:
                    continue

                if not fullname:
                    raise ValueError(
                        "Қате: Құжаттағы кестеден бұрын студенттің аты-жөні табылмады!"
                    )

                if not birth_date:
                    raise ValueError(
                        "Қате: Құжаттағы кестеден бұрын студенттің туған күні табылмады!"
                    )

                assessments = self._parse_table_rows(block)
                if assessments:
                    index += 1
                    students_cards.append(
                        {
                            "id": index,
                            "fullname": fullname,
                            "birth_date": birth_date,
                            "assessments": assessments,
                        }
                    )
                fullname, birth_date = "", ""

        return students_cards

    def _extract_birth_date(self, raw_value: str) -> str:
        if not raw_value:
            return ""
        clean_date = re.sub(r"[^0-9\.\-\/]", "", raw_value)
        return clean_date.strip(".").strip()

    def _parse_table_rows(self, table: Table) -> list[dict]:
        assessments = []
        for row in table.rows:
            cells = row.cells
            if len(cells) < 5:
                continue

            criterion_text = cells[0].text.strip()
            if "Құзыреттіліктер" in criterion_text or not criterion_text:
                continue

            assessments.append(
                {
                    "criterion": self._clean_spaces(criterion_text),
                    "start": self._clean_spaces(cells[1].text),
                    "mid": self._clean_spaces(cells[2].text),
                    "end": self._clean_spaces(cells[3].text),
                }
            )
        return assessments

    def _clean_meta_value(self, text: str, keyword: str) -> str:
        _, _, value = text.partition(keyword)
        value = value.strip(":. ")
        return self._clean_spaces(value)

    def _clean_spaces(self, text: str) -> str:
        if not text:
            return ""
        return re.sub(r"\s+", " ", text).strip()
