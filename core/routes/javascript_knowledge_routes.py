from tools.javascript_knowledge_tools import (
    update_javascript_knowledge,
    javascript_knowledge_status,
    generate_javascript_blueprint,
    create_javascript_starter_module,
    audit_javascript_file,
    explain_javascript_concept,
    generate_javascript_framework_translation,
    infer_javascript_action,
)


def _normalize(value: str) -> str:
    return " ".join((value or "").lower().strip().split())


def handle_javascript_knowledge_routes(user_input: str, text: str, clean_text: str):
    raw = _normalize(user_input)
    normalized = _normalize(text)
    clean = _normalize(clean_text)

    joined = " | ".join([raw, normalized, clean])

    # Exact command support.
    if raw in {
        "update javascript knowledge",
        "update js knowledge",
        "learn javascript",
        "learn js",
        "refresh javascript knowledge",
        "refresh js knowledge",
        "javascript knowledge update",
        "js knowledge update",
    }:
        return update_javascript_knowledge(force=False)

    if raw in {
        "force update javascript knowledge",
        "force update js knowledge",
        "relearn javascript knowledge",
        "relearn js knowledge",
        "force relearn javascript knowledge",
        "refresh all javascript knowledge",
        "refresh all js knowledge",
    }:
        return update_javascript_knowledge(force=True)

    if raw in {
        "javascript knowledge status",
        "js knowledge status",
        "javascript status",
        "js status",
        "show javascript knowledge status",
        "show js knowledge status",
        "check javascript knowledge",
        "check js knowledge",
    }:
        return javascript_knowledge_status()

    if raw.startswith("javascript blueprint "):
        request = user_input[len("javascript blueprint "):].strip()
        return generate_javascript_blueprint(request)

    if raw.startswith("js blueprint "):
        request = user_input[len("js blueprint "):].strip()
        return generate_javascript_blueprint(request)

    if raw.startswith("create javascript starter "):
        title = user_input[len("create javascript starter "):].strip()
        return create_javascript_starter_module(title)

    if raw.startswith("create js starter "):
        title = user_input[len("create js starter "):].strip()
        return create_javascript_starter_module(title)

    if raw.startswith("audit javascript file "):
        path = user_input[len("audit javascript file "):].strip()
        return audit_javascript_file(path)

    if raw.startswith("audit js file "):
        path = user_input[len("audit js file "):].strip()
        return audit_javascript_file(path)

    if raw.startswith("explain javascript "):
        concept = user_input[len("explain javascript "):].strip()
        return explain_javascript_concept(concept)

    if raw.startswith("explain js "):
        concept = user_input[len("explain js "):].strip()
        return explain_javascript_concept(concept)

    if raw.startswith("translate javascript "):
        request = user_input[len("translate javascript "):].strip()
        return generate_javascript_framework_translation(request)

    if raw.startswith("translate js "):
        request = user_input[len("translate js "):].strip()
        return generate_javascript_framework_translation(request)

    # Natural language support.
    action = infer_javascript_action(user_input)

    if action["action"] == "update":
        return update_javascript_knowledge(force=action.get("force", False))

    if action["action"] == "status":
        return javascript_knowledge_status()

    if action["action"] == "audit":
        path = action.get("path", "")

        if not path:
            return (
                "JAVASCRIPT AUDIT NEEDS A FILE\n"
                "I understood that you want a JavaScript audit, but I could not identify the file path.\n"
                "Example: Check whether resources/js/app.js is production ready"
            )

        return audit_javascript_file(path)

    if action["action"] == "explain":
        concept = action.get("concept", "")

        if not concept:
            return (
                "JAVASCRIPT EXPLANATION NEEDS A CONCEPT\n"
                "I understood that you want a JavaScript explanation, but I could not identify the concept.\n"
                "Example: Explain JavaScript promises\n"
                "Example: What is async await?"
            )

        return explain_javascript_concept(concept)

    if action["action"] == "starter":
        title = action.get("title", "Professional JavaScript Module")
        return create_javascript_starter_module(title)

    if action["action"] == "blueprint":
        request = action.get("request", user_input)
        return generate_javascript_blueprint(request)

    if action["action"] == "translate":
        request = action.get("request", user_input)
        return generate_javascript_framework_translation(request)

    # Guard: if this route was selected but the action is unclear, do not hallucinate.
    if (
        "javascript" in joined
        or "js" in joined
        or "ecmascript" in joined
        or "dom" in joined
        or "node" in joined
        or "react" in joined
        or "next" in joined
        or "vue" in joined
    ):
        return (
            "JAVASCRIPT REQUEST UNDERSTOOD, ACTION UNCLEAR\n"
            "I understood this is related to JavaScript, browser behavior, runtime logic, or frontend interactivity, "
            "but I need a clearer action.\n\n"
            "You can say things like:\n"
            "- Teach yourself the latest JavaScript from official sources\n"
            "- Create a JavaScript foundation for a company website\n"
            "- Check whether resources/js/app.js is production ready\n"
            "- Explain JavaScript promises\n"
            "- Translate this JavaScript logic to React\n"
            "- Build interactive website behavior using vanilla JavaScript"
        )

    return None
