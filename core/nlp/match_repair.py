def repair_matched_phrase(clean_text: str, intent: str, matched_phrase: str | None) -> str | None:
    text = clean_text.lower()

    if intent == "project_analysis":
        if "analyze project" in text:
            return "fix this"
        if "project health" in text:
            return "project health"

    if intent == "devops":
        if "nginx" in text:
            return "nginx problem"
        if "deployment" in text:
            return "deployment"
        if "log" in text:
            return "logs"

    if intent == "database":
        if "migration" in text:
            return "migration issue"
        if "sql" in text:
            return "sql"
        if "schema" in text:
            return "schema"

    if intent == "email":
        if "email" in text:
            return "client email"

    return matched_phrase
