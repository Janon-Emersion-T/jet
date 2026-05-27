ALIASES = {
    "fix this": "analyze project",
    "check this": "analyze project",
    "inspect this": "analyze project",
    "scan this": "analyze project",
    "make this better": "analyze project",
    "what is wrong": "analyze project",

    "check server": "server health check",
    "server issue": "server health check",
    "nginx problem": "nginx config inspector",
    "hosting problem": "hosting diagnostics",

    "db issue": "sql query analyzer",
    "database issue": "sql query analyzer",
    "migration issue": "migration analyzer",
    "mysql issue": "sql query analyzer",

    "write post": "social post",
    "write blog": "blog ideas",
    "write quotation": "generate quote",
    "client email": "draft client email",
}


def expand_alias(clean_text: str) -> str:
    text = clean_text.strip().lower()

    for alias, command in ALIASES.items():
        if alias in text:
            return command

    return clean_text
