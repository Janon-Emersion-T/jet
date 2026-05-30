import re
from typing import List

from core.routing.route_contracts import RouteDecision, RouteModule


def _normalize(text: str) -> str:
    return " ".join((text or "").lower().strip().split())


def _tokens(text: str):
    return set(re.findall(r"[a-zA-Z0-9_#+.-]+", _normalize(text)))


def _contains_phrase(text: str, phrase: str) -> bool:
    return _normalize(phrase) in _normalize(text)


def _keyword_score(text: str, module: RouteModule) -> float:
    text_norm = _normalize(text)
    text_tokens = _tokens(text_norm)

    score = 0.0

    for keyword in module.keywords:
        keyword_norm = _normalize(keyword)
        keyword_tokens = _tokens(keyword_norm)

        if not keyword_norm:
            continue

        if keyword_norm in text_norm:
            score += 0.35

        overlap = len(text_tokens.intersection(keyword_tokens))
        if overlap:
            score += min(0.20, overlap * 0.04)

    return score


def _canonical_score(text: str, module: RouteModule) -> float:
    score = 0.0

    for command in module.canonical_commands:
        command_norm = _normalize(command)

        if text == command_norm:
            score += 0.90
        elif text.startswith(command_norm):
            score += 0.75
        elif command_norm in text:
            score += 0.50

    return score


def _example_score(text: str, module: RouteModule) -> float:
    text_tokens = _tokens(text)

    if not text_tokens:
        return 0.0

    best = 0.0

    for example in module.examples:
        example_tokens = _tokens(example)

        if not example_tokens:
            continue

        overlap = len(text_tokens.intersection(example_tokens))
        ratio = overlap / max(len(example_tokens), 1)

        best = max(best, ratio * 0.30)

    return best


def _intent_score(nlp, module: RouteModule) -> float:
    detected_intent = _normalize(getattr(nlp, "intent", ""))
    detected_domain = _normalize(getattr(getattr(nlp, "domain", None), "domain", ""))

    score = 0.0

    if detected_intent and detected_intent in [_normalize(i) for i in module.intents]:
        score += 0.55

    if detected_domain and detected_domain == _normalize(module.domain):
        score += 0.25

    return score


def _build_text_candidates(user_input: str, nlp) -> List[str]:
    candidates = [
        user_input,
        getattr(nlp, "normalized_text", ""),
        getattr(nlp, "clean_text", ""),
        getattr(nlp, "canonical_command", ""),
    ]

    return [_normalize(candidate) for candidate in candidates if candidate]

def _specialist_boost(user_input: str, module: RouteModule) -> float:
    text = _normalize(user_input)

    if module.name == "html_knowledge":
        html_signals = [
            "html",
            "doctype",
            "section tag",
            "article tag",
            "html file",
            "sample html",
            "html knowledge",
            "latest html",
            "official sources",
            "living standard",
            "whatwg",
            "mdn",
            "web page structure",
            "landing page structure",
            "clean html foundation",
            "production ready",
            "written properly",
        ]

        if any(signal in text for signal in html_signals):
            return 0.35
    
    if module.name == "css_knowledge":
        css_signals = [
            "css",
            "stylesheet",
            "style sheet",
            "css file",
            "sample css",
            "css knowledge",
            "latest css",
            "official css",
            "w3c css",
            "mdn css",
            "css snapshot",
            "cascade",
            "specificity",
            "box model",
            "flexbox",
            "css grid",
            "grid layout",
            "media query",
            "media queries",
            "container query",
            "container queries",
            "custom properties",
            "css variables",
            "cascade layers",
            "css nesting",
            "responsive css",
            "design tokens",
            "production ready css",
        ]

        if any(signal in text for signal in css_signals):
            return 0.35

    return 0.0

def select_route(user_input: str, nlp, modules: List[RouteModule]) -> RouteDecision:
    candidates = _build_text_candidates(user_input, nlp)

    if not candidates:
        return RouteDecision(
            module=None,
            confidence=0.0,
            reason="No usable text candidates.",
            canonical_text="",
            scores={},
        )

    best_module = None
    best_score = 0.0
    best_reason = ""
    scores = {}

    for module in modules:
        module_score = 0.0
        reasons = []

        for text in candidates:
            canonical = _canonical_score(text, module)
            keyword = _keyword_score(text, module)
            example = _example_score(text, module)

            local_score = canonical + keyword + example

            if canonical:
                reasons.append(f"canonical={canonical:.2f}")
            if keyword:
                reasons.append(f"keyword={keyword:.2f}")
            if example:
                reasons.append(f"example={example:.2f}")

            module_score = max(module_score, local_score)


        intent = _intent_score(nlp, module)
        if intent:
            module_score += intent
            reasons.append(f"intent={intent:.2f}")

        boost = _specialist_boost(user_input, module)
        if boost:
            module_score += boost
            reasons.append(f"specialist_boost={boost:.2f}")

        module_score = min(module_score, 1.0)
        scores[module.name] = module_score

        if module_score > best_score:
            best_score = module_score
            best_module = module
            best_reason = ", ".join(reasons) or "best available match"

    threshold = 0.28

    if not best_module or best_score < threshold:
        return RouteDecision(
            module=None,
            confidence=best_score,
            reason="No module reached routing threshold.",
            canonical_text=getattr(nlp, "canonical_command", None) or getattr(nlp, "clean_text", None) or user_input,
            scores=scores,
        )

    return RouteDecision(
        module=best_module,
        confidence=best_score,
        reason=best_reason,
        canonical_text=getattr(nlp, "canonical_command", None) or getattr(nlp, "clean_text", None) or user_input,
        scores=scores,
    )
