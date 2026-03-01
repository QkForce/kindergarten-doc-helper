from docx import Document
from docx.oxml.text.paragraph import CT_P

from docx.document import Document as _Document
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph


def replace_placeholders_in_document(element, replacements):
    if hasattr(element, "paragraphs"):
        for paragraph in element.paragraphs:
            for key, value in replacements.items():
                placeholder = f"{{{{{key}}}}}"
                for run in paragraph.runs:
                    run.text = run.text.replace(placeholder, value)
    if hasattr(element, "tables"):
        for table in element.tables:
            for row in table.rows:
                for cell in row.cells:
                    replace_placeholders_in_document(cell, replacements)


def create_children_grow_cards(template_path, children_data, progress_callback=None):
    merged_doc = Document(template_path)
    replace_placeholders_in_document(merged_doc, children_data[0])
    merged_body = merged_doc.element.body
    total_children = len(children_data)

    if progress_callback:
        progress_callback(children_data[0]["fullname"], 1, total_children)

    for index, child_data in enumerate(children_data[1:]):
        if progress_callback:
            progress_callback(child_data["fullname"], index + 2, total_children)
        template_doc = Document(template_path)
        replace_placeholders_in_document(template_doc, child_data)
        merged_doc.add_page_break()

        sect_pr = merged_body.xpath("w:sectPr")[0]
        for element in template_doc.element.body:
            if "sectPr" in element.tag:
                continue
            if isinstance(element, CT_P) and not element.text.strip():
                continue
            merged_body.insert(merged_body.index(sect_pr), element)
    return merged_doc


def iter_block_items(parent):
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("Something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def fill_specific_child_in_big_file(doc, target_child_name, values, col_index=2):
    found_child = False

    for block in iter_block_items(doc):
        # 1. Search for a child's name (Paragraph)
        if isinstance(block, Paragraph) and "Баланың Т.А.Ә" in block.text:
            if target_child_name in block.text:
                found_child = True
            continue

        # 2. Fill in the table (Table)
        if isinstance(block, Table) and found_child:
            # Table Validation (Guard Clause)
            if not block.rows or "Құзыреттіліктер" not in block.cell(0, 0).text:
                continue

            # Table populating logic
            for i, val in enumerate(values, start=1):
                try:
                    block.cell(i, col_index).text = str(val)
                except IndexError:
                    print(f"Қате: {target_child_name} үшін жол ({i}) табылған жоқ")

            # After filling, we reset the status.
            found_child = False

    return doc


def fill_all_children_in_big_file(
    docx_path, children_data, col_index, progress_callback=None
):
    doc = Document(docx_path)
    index = 1
    total_children = len(children_data)
    for child in children_data:
        child_name = child["fullname"]
        values = [v for k, v in child.items() if k != "fullname"]
        if progress_callback:
            progress_callback(child_name, index, total_children)
        doc = fill_specific_child_in_big_file(doc, child_name, values, col_index)
        index += 1

    return doc
