from tools.ticket_prioritization_tools import ticket_prioritization_engine


def handle_ticket_prioritization_routes(user_input: str, text: str, clean_text: str):
    if text in [
        "ticket prioritization engine",
        "prioritize tickets",
        "ticket priority engine",
        "analyze ticket priority",
        "support ticket priority",
    ]:
        return ticket_prioritization_engine()

    if text in ["351 help", "phase 351 help", "ticket prioritization help"]:
        return """TICKET PRIORITIZATION ENGINE COMMANDS — PHASE 351

351. ticket prioritization engine
     prioritize tickets
     ticket priority engine
     analyze ticket priority
     support ticket priority
"""

    return None
