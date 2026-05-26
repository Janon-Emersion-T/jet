from tools.invoice_ocr_tools import invoice_ocr_assistant


def handle_invoice_ocr_routes(user_input: str, text: str, clean_text: str):
    if text in ["invoice ocr assistant", "invoice ocr", "scan invoices", "read invoices"]:
        return invoice_ocr_assistant()

    if text in ["343 help", "phase 343 help", "invoice ocr help"]:
        return """INVOICE OCR COMMANDS — PHASE 343

343. invoice ocr assistant
     invoice ocr
     scan invoices
     read invoices
"""

    return None
