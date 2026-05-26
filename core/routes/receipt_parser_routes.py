from tools.receipt_parser_tools import receipt_parser


def handle_receipt_parser_routes(user_input: str, text: str, clean_text: str):
    if text in ["receipt parser", "parse receipts", "read receipts", "receipt scanner"]:
        return receipt_parser()

    if text in ["344 help", "phase 344 help", "receipt parser help"]:
        return """RECEIPT PARSER COMMANDS — PHASE 344

344. receipt parser
     parse receipts
     read receipts
     receipt scanner
"""

    return None
