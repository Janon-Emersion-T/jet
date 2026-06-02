from tools.programming_knowledge_tools import (
    infer_programming_knowledge_action,
    list_programming_topics,
    programming_knowledge_status,
    update_all_programming_knowledge,
    update_programming_topic,
)
from core.autonomous_learning import (
    autonomous_learning_status,
    enable_autonomous_learning,
    disable_autonomous_learning,
    run_autonomous_learning_cycle,
)


def _normalize(value: str) -> str:
    return " ".join((value or "").lower().strip().split())


def handle_programming_knowledge_routes(user_input: str, text: str, clean_text: str):
    raw = _normalize(user_input)

    if raw in {
        "update all programming knowledge",
        "learn all programming languages",
        "learn all programming frameworks",
        "learn all programming languages and frameworks",
        "learn all learning topics",
        "learn all 200 topics",
        "teach yourself all programming languages",
        "teach yourself all programming languages and frameworks",
    }:
        return update_all_programming_knowledge(force=False, trigger="manual-route")

    if raw in {
        "force update all programming knowledge",
        "force relearn all programming knowledge",
        "refresh all programming knowledge",
    }:
        return update_all_programming_knowledge(force=True, trigger="manual-route")

    if raw in {
        "programming knowledge status",
        "programming languages status",
        "show programming knowledge status",
        "learning curriculum status",
    }:
        return programming_knowledge_status()

    if raw in {
        "autonomous learning status",
        "show autonomous learning status",
        "background learning status",
    }:
        return autonomous_learning_status()

    if raw in {
        "start autonomous learning",
        "enable autonomous learning",
        "start background learning",
    }:
        return enable_autonomous_learning()

    if raw in {
        "stop autonomous learning",
        "disable autonomous learning",
        "stop background learning",
    }:
        return disable_autonomous_learning()

    if raw in {
        "run autonomous learning cycle",
        "run background learning now",
    }:
        run_autonomous_learning_cycle()
        return autonomous_learning_status()

    action = infer_programming_knowledge_action(user_input)

    if action["action"] == "update_all":
        return update_all_programming_knowledge(
            force=action.get("force", False),
            trigger="natural-language",
        )

    if action["action"] == "status_all":
        return programming_knowledge_status()

    if action["action"] == "update":
        return update_programming_topic(
            action.get("topic", ""),
            force=action.get("force", False),
            trigger="natural-language",
        )

    if action["action"] == "status":
        return programming_knowledge_status(action.get("topic"))

    joined = " | ".join({_normalize(user_input), _normalize(text), _normalize(clean_text)})
    if "learn " in joined or "programming" in joined or "curriculum" in joined or "teaching session" in joined:
        available = ", ".join(list_programming_topics())
        return (
            "AUTONOMOUS LEARNING REQUEST UNDERSTOOD, ACTION UNCLEAR\n"
            "I understood this is about automated learning, but I need a clearer action.\n\n"
            "You can say things like:\n"
            "- Learn python\n"
            "- Learn how computers actually work\n"
            "- Learn software architecture fundamentals\n"
            "- Learn rust\n"
            "- Learn laravel\n"
            "- Learn all 200 topics\n"
            "- Python knowledge status\n\n"
            f"Available topics: {available}"
        )

    return None
