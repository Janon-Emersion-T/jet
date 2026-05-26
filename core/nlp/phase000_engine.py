from dataclasses import dataclass, field
from typing import Dict, List, Optional

from core.nlp.phase000a_foundation_router import analyze_foundation_command
from core.nlp.phase000b_semantic_router import (
    classify_with_embeddings,
    semantic_entities,
    semantic_tokenize,
)


@dataclass
class NLPResult:
    original_text: str
    normalized_text: str
    clean_text: str
    tokens: List[str]
    intent: str
    confidence: float
    canonical_command: Optional[str] = None
    entities: Dict[str, str] = field(default_factory=dict)
    matched_phrase: Optional[str] = None
    safety_level: str = "safe"
    engine: str = "phase000"


def analyze_command(user_input: str) -> NLPResult:
    foundation = analyze_foundation_command(user_input)

    semantic_intent, semantic_score, semantic_phrase = classify_with_embeddings(
        foundation.normalized_text
    )

    tokens = semantic_tokenize(foundation.normalized_text) or foundation.tokens
    entities = foundation.entities
    entities.update(semantic_entities(foundation.normalized_text))

    intent = foundation.intent
    confidence = foundation.confidence
    matched_phrase = foundation.matched_phrase
    engine = foundation.engine

    if semantic_score > confidence:
        intent = semantic_intent
        confidence = semantic_score
        matched_phrase = semantic_phrase
        engine = "nlp-000b-transformer-semantic"

    if foundation.canonical_command:
        intent = "command"
        confidence = max(confidence, foundation.confidence)
        matched_phrase = foundation.matched_phrase
        engine = "nlp-000a-canonical-command"

    return NLPResult(
        original_text=foundation.original_text,
        normalized_text=foundation.normalized_text,
        clean_text=foundation.clean_text,
        tokens=tokens,
        intent=intent,
        confidence=round(float(confidence), 3),
        canonical_command=foundation.canonical_command,
        entities=entities,
        matched_phrase=matched_phrase,
        safety_level=foundation.safety_level,
        engine=engine,
    )


def classify_intent_nlp(user_input: str) -> str:
    return analyze_command(user_input).intent


def format_nlp_report(user_input: str) -> str:
    result = analyze_command(user_input)

    entity_lines = [
        f"- {key}: {value}"
        for key, value in result.entities.items()
    ]

    entities = "\n".join(entity_lines) if entity_lines else "- None detected"

    return f"""PHASE NLP-000A + NLP-000B REPORT

Original:
{result.original_text}

Normalized:
{result.normalized_text}

Clean routing text:
{result.clean_text}

Intent: {result.intent}
Confidence: {result.confidence}
Canonical command: {result.canonical_command or 'None'}
Matched phrase: {result.matched_phrase or 'None'}
Safety level: {result.safety_level}
Engine: {result.engine}

Entities:
{entities}

Tokens:
{', '.join(result.tokens) if result.tokens else 'None'}"""
