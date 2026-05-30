from tools.html_knowledge_tools import (
    update_html_knowledge,
    html_knowledge_status,
    generate_html_blueprint,
    create_html_starter_page,
    audit_html_file,
    explain_html_element,
)


def _normalize(value: str) -> str:
    return " ".join((value or "").lower().strip().split())


def _matches_any(candidates, exact_phrases):
    return any(candidate in exact_phrases for candidate in candidates)


def _starts_with_any(candidates, prefixes):
    for candidate in candidates:
        for prefix in prefixes:
            if candidate.startswith(prefix):
                return candidate, prefix
    return None, None


def _extract_after_original(user_input: str, trigger: str) -> str:
    if user_input.lower().strip().startswith(trigger):
        return user_input.strip()[len(trigger):].strip()
    return ""


def handle_html_knowledge_routes(user_input: str, text: str, clean_text: str):
    """
    HTML Knowledge Engine route handler.

    Important:
    We check user_input, text, and clean_text because JARVIS NLP may rewrite
    commands such as "update html knowledge" into another canonical action.
    For knowledge commands, the original user_input must always win.
    """

    raw = _normalize(user_input)
    normalized = _normalize(text)
    clean = _normalize(clean_text)

    candidates = [raw, normalized, clean]

    # -------------------------
    # HTML knowledge update
    # -------------------------
    if _matches_any(
        candidates,
        {
            "update html knowledge",
            "learn html",
            "refresh html knowledge",
            "update the html knowledge",
            "learn html knowledge",
            "html knowledge update",
        },
    ):
        return update_html_knowledge(force=False)

    if _matches_any(
        candidates,
        {
            "force update html knowledge",
            "relearn html knowledge",
            "force relearn html knowledge",
            "refresh all html knowledge",
            "force refresh html knowledge",
        },
    ):
        return update_html_knowledge(force=True)

    # -------------------------
    # HTML knowledge status
    # -------------------------
    if _matches_any(
        candidates,
        {
            "html knowledge status",
            "html status",
            "show html knowledge status",
            "check html knowledge",
        },
    ):
        return html_knowledge_status()

    # -------------------------
    # HTML blueprint
    # -------------------------
    matched, prefix = _starts_with_any(
        candidates,
        {
            "html blueprint ",
            "create html blueprint ",
            "plan html ",
            "html plan ",
        },
    )

    if matched:
        # Use original text to preserve capitalization and full request.
        for trigger in [
            "html blueprint ",
            "create html blueprint ",
            "plan html ",
            "html plan ",
        ]:
            request = _extract_after_original(user_input, trigger)
            if request:
                return generate_html_blueprint(request)

        # Fallback if NLP changed casing/wording
        request = matched.replace(prefix, "", 1).strip()
        return generate_html_blueprint(request)

    # -------------------------
    # HTML starter page
    # -------------------------
    matched, prefix = _starts_with_any(
        candidates,
        {
            "create html starter ",
            "generate html starter ",
            "html starter ",
            "create starter html ",
        },
    )

    if matched:
        for trigger in [
            "create html starter ",
            "generate html starter ",
            "html starter ",
            "create starter html ",
        ]:
            title = _extract_after_original(user_input, trigger)
            if title:
                return create_html_starter_page(title)

        title = matched.replace(prefix, "", 1).strip()
        return create_html_starter_page(title)

    # -------------------------
    # HTML file audit
    # -------------------------
    matched, prefix = _starts_with_any(
        candidates,
        {
            "audit html file ",
            "check html file ",
            "validate html file ",
            "review html file ",
        },
    )

    if matched:
        for trigger in [
            "audit html file ",
            "check html file ",
            "validate html file ",
            "review html file ",
        ]:
            path = _extract_after_original(user_input, trigger)
            if path:
                return audit_html_file(path)

        path = matched.replace(prefix, "", 1).strip()
        return audit_html_file(path)

    # -------------------------
    # HTML element explanation
    # -------------------------
    matched, prefix = _starts_with_any(
        candidates,
        {
            "explain html element ",
            "html element ",
            "explain tag ",
            "explain html tag ",
        },
    )

    if matched:
        for trigger in [
            "explain html element ",
            "html element ",
            "explain tag ",
            "explain html tag ",
        ]:
            element = _extract_after_original(user_input, trigger)
            if element:
                return explain_html_element(element)

        element = matched.replace(prefix, "", 1).strip()
        return explain_html_element(element)

    return None
