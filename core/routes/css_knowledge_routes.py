from tools.css_knowledge_tools import (
    update_css_knowledge,
    css_knowledge_status,
    generate_css_blueprint,
    create_css_starter_stylesheet,
    audit_css_file,
    explain_css_concept,
    generate_css_framework_translation,
    infer_css_action,
)


def _normalize(value: str) -> str:
    return " ".join((value or "").lower().strip().split())


def handle_css_knowledge_routes(user_input: str, text: str, clean_text: str):
    raw = _normalize(user_input)
    normalized = _normalize(text)
    clean = _normalize(clean_text)

    candidates = [raw, normalized, clean]
    joined = " | ".join(candidates)

    # Exact command support.
    if raw in {
        "update css knowledge",
        "learn css",
        "refresh css knowledge",
        "update the css knowledge",
        "css knowledge update",
    }:
        return update_css_knowledge(force=False)

    if raw in {
        "force update css knowledge",
        "relearn css knowledge",
        "force relearn css knowledge",
        "refresh all css knowledge",
    }:
        return update_css_knowledge(force=True)

    if raw in {
        "css knowledge status",
        "css status",
        "show css knowledge status",
        "check css knowledge",
    }:
        return css_knowledge_status()

    if raw.startswith("css blueprint "):
        request = user_input[len("css blueprint "):].strip()
        return generate_css_blueprint(request)

    if raw.startswith("create css starter "):
        title = user_input[len("create css starter "):].strip()
        return create_css_starter_stylesheet(title)

    if raw.startswith("audit css file "):
        path = user_input[len("audit css file "):].strip()
        return audit_css_file(path)

    if raw.startswith("explain css "):
        concept = user_input[len("explain css "):].strip()
        return explain_css_concept(concept)

    if raw.startswith("translate css "):
        request = user_input[len("translate css "):].strip()
        return generate_css_framework_translation(request)

    # Natural language support.
    action = infer_css_action(user_input)

    if action["action"] == "update":
        return update_css_knowledge(force=action.get("force", False))

    if action["action"] == "status":
        return css_knowledge_status()

    if action["action"] == "audit":
        path = action.get("path", "")

        if not path:
            return (
                "CSS AUDIT NEEDS A FILE\n"
                "I understood that you want a CSS audit, but I could not identify the file path.\n"
                "Example: Check whether resources/css/app.css is production ready"
            )

        return audit_css_file(path)

    if action["action"] == "explain":
        concept = action.get("concept", "")

        if not concept:
            return (
                "CSS EXPLANATION NEEDS A CONCEPT\n"
                "I understood that you want a CSS explanation, but I could not identify the concept.\n"
                "Example: Explain CSS cascade\n"
                "Example: What is the correct use of container queries?"
            )

        return explain_css_concept(concept)

    if action["action"] == "starter":
        title = action.get("title", "Professional Website")
        return create_css_starter_stylesheet(title)

    if action["action"] == "blueprint":
        request = action.get("request", user_input)
        return generate_css_blueprint(request)

    if action["action"] == "translate":
        request = action.get("request", user_input)
        return generate_css_framework_translation(request)

    # Guard: if this route was selected but the action is unclear, do not hallucinate.
    if "css" in joined or "stylesheet" in joined or "style" in joined:
        return (
            "CSS REQUEST UNDERSTOOD, ACTION UNCLEAR\n"
            "I understood this is related to CSS, styling, layout, or frontend design, but I need a clearer action.\n\n"
            "You can say things like:\n"
            "- Teach yourself the latest CSS from official sources\n"
            "- Create a modern CSS foundation for a company website\n"
            "- Check whether resources/css/app.css is production ready\n"
            "- Explain CSS cascade\n"
            "- Explain container queries\n"
            "- Translate this CSS architecture to Tailwind"
        )

    return None
