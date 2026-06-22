import re
from docx import Document
from docx.document import Document as _Document
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from docx.oxml import CT_P, CT_Tbl


class GrowCardParser:
    def __init__(self, file_path: str):
        self.doc = Document(file_path)

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

    def parse(self) -> list[dict]:
        students_cards = []
        current_meta = {"fullname": "", "birth_date": "", "group_name": ""}
        for block in self.iter_block_items(self.doc):
            if isinstance(block, Paragraph):
                text = block.text.strip()
                if not text:
                    continue
                if "Баланың Т.А.Ә" in text or "Т.А.Ә" in text:
                    current_meta["fullname"] = self._clean_meta_value(text, "Т.А.Ә")
                elif "туған жылы" in text or "күні" in text or "«" in text:
                    keyword = "күні" if "күні" in text else "жылы"
                    raw_value = self._clean_meta_value(text, keyword)
                    if "«" in raw_value and "»" in raw_value:
                        group_match = re.search(r"«[^»]+»\s*\w*\s*\w*", raw_value)
                        if group_match:
                            g_name = group_match.group(0).strip()
                            current_meta["group_name"] = g_name
                            raw_date = raw_value.replace(g_name, "").strip()
                            current_meta["birth_date"] = self._extract_birth_date(
                                raw_date
                            )
                    else:
                        current_meta["birth_date"] = self._extract_birth_date(raw_value)
            elif isinstance(block, Table):
                if not block.rows or "Құзыреттіліктер" not in block.cell(0, 0).text:
                    continue
                assessments = self._parse_table_rows(block)
                if assessments:
                    students_cards.append(
                        {
                            "fullname": current_meta["fullname"] or "Анықталмады",
                            "birth_date": current_meta["birth_date"] or "Анықталмады",
                            "group_name": current_meta["group_name"] or "Анықталмады",
                            "assessments": assessments,
                        }
                    )
                current_meta = {"fullname": "", "birth_date": "", "group_name": ""}
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
