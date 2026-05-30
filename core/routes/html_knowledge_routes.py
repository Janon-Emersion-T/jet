from tools.html_knowledge_tools import (
    update_html_knowledge,
    html_knowledge_status,
    generate_html_blueprint,
    create_html_starter_page,
    audit_html_file,
    explain_html_element,
    infer_html_action,
)


def _normalize(value: str) -> str:
    return " ".join((value or "").lower().strip().split())


def _first_non_empty(*values):
    for value in values:
        if value:
            return value
    return ""


def handle_html_knowledge_routes(user_input: str, text: str, clean_text: str):
    raw = _normalize(user_input)
    normalized = _normalize(text)
    clean = _normalize(clean_text)

    candidates = [raw, normalized, clean]

    joined = " | ".join(candidates)

    # Exact command support still remains.
    if raw in {
        "update html knowledge",
        "learn html",
        "refresh html knowledge",
        "update the html knowledge",
        "html knowledge update",
    }:
        return update_html_knowledge(force=False)

    if raw in {
        "force update html knowledge",
        "relearn html knowledge",
        "force relearn html knowledge",
        "refresh all html knowledge",
    }:
        return update_html_knowledge(force=True)

    if raw in {
        "html knowledge status",
        "html status",
        "show html knowledge status",
        "check html knowledge",
    }:
        return html_knowledge_status()

    if raw.startswith("html blueprint "):
        request = user_input[len("html blueprint "):].strip()
        return generate_html_blueprint(request)

    if raw.startswith("create html starter "):
        title = user_input[len("create html starter "):].strip()
        return create_html_starter_page(title)

    if raw.startswith("audit html file "):
        path = user_input[len("audit html file "):].strip()
        return audit_html_file(path)

    if raw.startswith("explain html element "):
        element = user_input[len("explain html element "):].strip()
        return explain_html_element(element)

    # Natural language support.
    action = infer_html_action(user_input)

    if action["action"] == "update":
        return update_html_knowledge(force=action.get("force", False))

    if action["action"] == "status":
        return html_knowledge_status()

    if action["action"] == "audit":
        path = action.get("path", "")

        if not path:
            return (
                "HTML AUDIT NEEDS A FILE\n"
                "I understood that you want an HTML audit, but I could not identify the file path.\n"
                "Example: Check whether test_documents/sample.html is written properly"
            )

        return audit_html_file(path)

    if action["action"] == "explain":
        element = action.get("element", "")

        if not element:
            return (
                "HTML ELEMENT EXPLANATION NEEDS AN ELEMENT\n"
                "I understood that you want an HTML explanation, but I could not identify the element.\n"
                "Example: What is the correct use of the section tag?"
            )

        return explain_html_element(element)

    if action["action"] == "starter":
        title = action.get("title", "Professional Website")
        return create_html_starter_page(title)

    if action["action"] == "blueprint":
        request = action.get("request", user_input)
        return generate_html_blueprint(request)

    # Guard: if this route was selected but the action is unclear, do not hallucinate.
    if "html" in joined or "website" in joined or "web page" in joined or "landing page" in joined:
        return (
            "HTML REQUEST UNDERSTOOD, ACTION UNCLEAR\n"
            "I understood this is related to HTML or website structure, but I need a clearer action.\n\n"
            "You can say things like:\n"
            "- Teach yourself the latest HTML properly from official sources\n"
            "- Create the basic structure for a professional website\n"
            "- Check whether test_documents/sample.html is written properly\n"
            "- Explain when I should use article instead of section"
        )

    return None