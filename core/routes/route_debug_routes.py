from core.routing.route_registry import get_route_modules
from core.routing.nlp_route_selector import select_route
from core.nlp.unified_orchestrator import orchestrate_command


def debug_route_command(user_input: str) -> str:
    query = user_input.strip()
    nlp = orchestrate_command(query)
    decision = select_route(query, nlp, get_route_modules())

    lines = [
        "ROUTE DEBUG REPORT",
        "",
        f"Original: {query}",
        f"Normalized: {getattr(nlp, 'normalized_text', '-')}",
        f"Clean text: {getattr(nlp, 'clean_text', '-')}",
        f"Canonical: {getattr(nlp, 'canonical_command', '-')}",
        f"Intent: {getattr(nlp, 'intent', '-')}",
        f"NLP confidence: {getattr(nlp, 'confidence', '-')}",
        "",
        f"Selected module: {decision.module.name if decision.module else 'None'}",
        f"Routing confidence: {decision.confidence}",
        f"Reason: {decision.reason}",
        "",
        "Top scores:",
    ]

    top_scores = sorted(decision.scores.items(), key=lambda item: item[1], reverse=True)[:10]

    for name, score in top_scores:
        lines.append(f"- {name}: {score:.2f}")

    return "\n".join(lines)
