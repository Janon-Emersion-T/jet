def apply_priority_score(intent: str, clean_text: str) -> str:
    text = clean_text.lower()

    project_words = [
        "fix this",
        "check this",
        "inspect this",
        "scan this",
        "make this better",
        "what is wrong",
        "analyze project",
        "project health",
    ]

    devops_words = ["nginx", "server", "hosting", "deploy", "deployment", "log", "disk"]
    database_words = ["migration", "mysql", "database", "schema", "sql", "eloquent", "n+1", "n plus one"]
    email_words = ["client email", "email", "mail", "gmail", "inbox", "reply", "draft email"]
    content_words = ["blog", "seo", "post", "proposal", "quote", "quotation", "content"]

    if any(word in text for word in project_words):
        return "project_analysis"

    if any(word in text for word in devops_words):
        return "devops"

    if any(word in text for word in database_words):
        return "database"

    if any(word in text for word in email_words):
        return "email"

    if any(word in text for word in content_words):
        return "content"

    return intent
