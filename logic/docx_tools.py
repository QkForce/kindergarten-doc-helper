from docx import Document
from docx.oxml.text.paragraph import CT_P


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
