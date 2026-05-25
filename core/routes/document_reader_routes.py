from tools.document_reader_tools import (
    local_document_search,
    read_pdf,
    read_docx,
    read_spreadsheet,
    image_ocr_option,
    screenshot_understanding_status,
    document_reader_help,
)


def handle_document_reader_routes(user_input: str, text: str, clean_text: str):
    if text in ["document reader help", "local document help"]:
        return document_reader_help()

    if text.startswith("search documents for "):
        query = user_input.replace("search documents for ", "", 1).strip()
        return local_document_search(query)

    if text.startswith("read pdf "):
        path = user_input.replace("read pdf ", "", 1).strip()
        return read_pdf(path)

    if text.startswith("read docx "):
        path = user_input.replace("read docx ", "", 1).strip()
        return read_docx(path)

    if text.startswith("read spreadsheet "):
        path = user_input.replace("read spreadsheet ", "", 1).strip()
        return read_spreadsheet(path)

    if text.startswith("image ocr option "):
        path = user_input.replace("image ocr option ", "", 1).strip()
        return image_ocr_option(path)

    if text in ["screenshot understanding status", "screenshot understanding"]:
        return screenshot_understanding_status()
    
    if text.startswith("read image text "):
        path = user_input.replace("read image text ", "", 1).strip()
        return image_ocr_option(path)

    return None
