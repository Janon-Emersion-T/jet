import re
import string
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple


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


try:
    import spacy
except Exception:
    spacy = None

try:
    from sentence_transformers import SentenceTransformer, util
except Exception:
    SentenceTransformer = None
    util = None

try:
    import torch
except Exception:
    torch = None


_SPACY_MODEL = None
_EMBEDDING_MODEL = None


INTENT_EXAMPLES = {
    "weather": [
        "what is the weather",
        "is it raining",
        "show me the forecast",
        "check temperature",
    ],
    "location": [
        "where am i",
        "show my current location",
        "which country am i in",
    ],
    "camera": [
        "open camera",
        "scan the room",
        "look around",
        "can you see me",
    ],
    "email": [
        "check my email",
        "send an email",
        "open gmail",
        "read inbox",
    ],
    "calendar": [
        "show my calendar",
        "schedule a meeting",
        "create appointment",
    ],
    "browser_control": [
        "open google",
        "open youtube",
        "open github",
        "visit website",
        "launch browser",
    ],
    "google_search": [
        "search google for laravel",
        "google search ai news",
        "search for documentation",
        "look up this online",
    ],
    "project_analysis": [
        "analyze this project",
        "scan project structure",
        "check project health",
        "inspect the codebase",
    ],
    "patch_workflow": [
        "apply patch",
        "show file diff",
        "compare patch",
        "rollback proposal",
        "confirm before write",
    ],
    "devops": [
        "git status",
        "check nginx",
        "deployment assistant",
        "server logs",
        "disk cleanup",
    ],
    "database": [
        "analyze sql query",
        "database schema",
        "migration rollback",
        "n plus one detector",
        "eloquent optimization",
    ],
    "content": [
        "write blog ideas",
        "generate seo brief",
        "draft social post",
        "create proposal",
        "write case study",
    ],
    "memory": [
        "remember this",
        "save this memory",
        "what do you remember",
        "forget this",
    ],
    "task": [
        "create task",
        "show todos",
        "remind me",
        "deadline tracker",
    ],
    "nlp": [
        "analyze command",
        "parse intent",
        "test nlp",
        "understand this command",
    ],
    "general": [
        "answer this",
        "explain this",
        "help me",
    ],
}


CANONICAL_COMMANDS = {
    "capabilities": [
        "capabilities",
        "list capabilities",
        "what can you do",
        "show abilities",
    ],
    "show current folder": [
        "show current folder",
        "where am i",
        "current directory",
        "pwd",
    ],
    "list files": [
        "list files",
        "show files",
        "ls",
        "show directory files",
    ],
    "show disk usage": [
        "show disk usage",
        "disk usage",
        "check disk",
        "storage usage",
    ],
    "show memory usage": [
        "show memory usage",
        "memory usage",
        "ram usage",
        "check memory",
    ],
    "show date": [
        "show date",
        "date",
        "today date",
    ],
    "who am i": [
        "who am i",
        "current user",
    ],
    "python version": [
        "python version",
        "check python",
        "python --version",
    ],
    "node version": [
        "node version",
        "check node",
        "node --version",
    ],
    "npm version": [
        "npm version",
        "check npm",
        "npm --version",
    ],
    "activate voice mode": [
        "activate voice mode",
        "start voice mode",
        "voice mode",
    ],
}


TYPO_CORRECTIONS = {
    "jarwis": "jarvis",
    "jervis": "jarvis",
    "javris": "jarvis",
    "opne": "open",
    "opeb": "open",
    "serach": "search",
    "seach": "search",
    "gogle": "google",
    "googl": "google",
    "yt": "youtube",
    "shutdon": "shutdown",
    "capabilites": "capabilities",
    "memor": "memory",
    "rember": "remember",
    "projec": "project",
    "anlyze": "analyze",
    "analize": "analyze",
    "optimise": "optimize",
    "optimisation": "optimization",
    "deployement": "deployment",
    "erro": "error",
}


DANGEROUS_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bsudo\s+rm\b",
    r"\bmkfs\b",
    r"\bdd\s+if=",
    r"\bshutdown\s+now\b",
    r"\breboot\b",
    r"\bchmod\s+777\s+/\b",
    r"\bchown\s+.*\s+/\b",
    r"\bformat\s+disk\b",
]


def normalize_text(user_input: str) -> str:
    text = unicodedata.normalize("NFKC", user_input or "")
    text = text.replace("’", "'").replace("`", "'").replace("\u2014", "-")
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def correct_typos(text: str) -> str:
    words = text.split()
    corrected = []

    for word in words:
        stripped = word.strip(string.punctuation)
        replacement = TYPO_CORRECTIONS.get(stripped, stripped)

        if stripped != replacement:
            word = word.replace(stripped, replacement)

        corrected.append(word)

    return " ".join(corrected)


def clean_for_routing(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation)).strip()


def get_spacy_model():
    global _SPACY_MODEL

    if _SPACY_MODEL is not None:
        return _SPACY_MODEL

    if spacy is None:
        return None

    for model_name in [
        "en_core_web_trf",
        "en_core_web_sm",
    ]:
        try:
            _SPACY_MODEL = spacy.load(model_name)
            return _SPACY_MODEL
        except Exception:
            continue

    return None


def get_embedding_model():
    global _EMBEDDING_MODEL

    if _EMBEDDING_MODEL is not None:
        return _EMBEDDING_MODEL

    if SentenceTransformer is None:
        return None

    try:
        _EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        return _EMBEDDING_MODEL
    except Exception:
        return None


def tokenize(text: str) -> List[str]:
    nlp = get_spacy_model()

    if nlp:
        doc = nlp(text)
        return [
            token.lemma_.lower()
            for token in doc
            if not token.is_stop and not token.is_punct and token.text.strip()
        ]

    clean = clean_for_routing(text)
    return [word for word in clean.split() if word]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def detect_safety_level(text: str) -> str:
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, text):
            return "dangerous"

    destructive_words = [
        "delete",
        "remove",
        "wipe",
        "format",
        "kill",
        "terminate",
        "overwrite",
    ]

    if any(word in text for word in destructive_words):
        return "needs_confirmation"

    return "safe"


def extract_entities(text: str) -> Dict[str, str]:
    entities = {}

    url_match = re.search(r"https?://\S+", text)
    if url_match:
        entities["url"] = url_match.group(0).rstrip(".,)")

    file_match = re.search(
        r"([\w\-/]+\.(?:py|php|js|ts|jsx|tsx|md|txt|json|env|html|css|sql|blade\.php))",
        text,
    )
    if file_match:
        entities["file"] = file_match.group(1)

    phase_match = re.search(
        r"\b(?:phase|phases)\s*(\d{1,4})(?:\s*[-–]\s*(\d{1,4}))?\b",
        text,
    )
    if phase_match:
        entities["phase_start"] = phase_match.group(1)
        if phase_match.group(2):
            entities["phase_end"] = phase_match.group(2)

    quoted_match = re.search(r"['\"]([^'\"]+)['\"]", text)
    if quoted_match:
        entities["quoted_text"] = quoted_match.group(1)

    nlp = get_spacy_model()
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            key = f"entity_{ent.label_.lower()}"
            entities[key] = ent.text

    return entities


def detect_canonical_command(clean_text: str) -> Tuple[Optional[str], float, Optional[str]]:
    best_command = None
    best_score = 0.0
    best_phrase = None

    for canonical, phrases in CANONICAL_COMMANDS.items():
        for phrase in phrases:
            phrase_clean = clean_for_routing(phrase)
            score = similarity(clean_text, phrase_clean)

            if clean_text == phrase_clean:
                score = 1.0
            elif phrase_clean in clean_text or clean_text in phrase_clean:
                score = max(score, 0.88)

            if score > best_score:
                best_command = canonical
                best_score = score
                best_phrase = phrase

    if best_score >= 0.82:
        return best_command, best_score, best_phrase

    return None, 0.0, None


def classify_with_embeddings(text: str) -> Tuple[str, float, Optional[str]]:
    model = get_embedding_model()

    if model is None or util is None:
        return "general", 0.0, None

    try:
        input_embedding = model.encode(text, convert_to_tensor=True)

        best_intent = "general"
        best_score = 0.0
        best_phrase = None

        for intent, examples in INTENT_EXAMPLES.items():
            example_embeddings = model.encode(examples, convert_to_tensor=True)
            scores = util.cos_sim(input_embedding, example_embeddings)[0]

            max_score = float(scores.max())
            best_index = int(scores.argmax())

            if max_score > best_score:
                best_intent = intent
                best_score = max_score
                best_phrase = examples[best_index]

        if best_score < 0.40:
            return "general", best_score, best_phrase

        return best_intent, best_score, best_phrase

    except Exception:
        return "general", 0.0, None


def classify_with_keywords(text: str, clean_text: str, tokens: List[str]) -> Tuple[str, float, Optional[str]]:
    best_intent = "general"
    best_score = 0.0
    best_phrase = None
    token_set = set(tokens)

    for intent, examples in INTENT_EXAMPLES.items():
        for phrase in examples:
            phrase_clean = clean_for_routing(phrase)
            phrase_tokens = set(phrase_clean.split())

            if phrase in text or phrase_clean in clean_text:
                score = 0.96
            elif phrase_tokens and phrase_tokens.issubset(token_set):
                score = 0.90
            else:
                score = similarity(clean_text, phrase_clean)

            if score > best_score:
                best_intent = intent
                best_score = score
                best_phrase = phrase

    if best_score < 0.55:
        return "general", best_score, best_phrase

    return best_intent, best_score, best_phrase


def analyze_command(user_input: str) -> NLPResult:
    normalized = normalize_text(user_input)
    corrected = correct_typos(normalized)
    clean = clean_for_routing(corrected)
    tokens = tokenize(corrected)
    entities = extract_entities(corrected)
    safety_level = detect_safety_level(corrected)

    canonical_command, canonical_score, canonical_phrase = detect_canonical_command(clean)

    embedding_intent, embedding_score, embedding_phrase = classify_with_embeddings(corrected)
    keyword_intent, keyword_score, keyword_phrase = classify_with_keywords(corrected, clean, tokens)

    if embedding_score >= keyword_score:
        intent = embedding_intent
        confidence = embedding_score
        matched_phrase = embedding_phrase
        engine = "sentence-transformers"
    else:
        intent = keyword_intent
        confidence = keyword_score
        matched_phrase = keyword_phrase
        engine = "keyword-fallback"

    if canonical_command and canonical_score >= max(confidence, 0.82):
        clean = canonical_command
        corrected = canonical_command
        intent = "command"
        confidence = canonical_score
        matched_phrase = canonical_phrase
        engine = "canonical-command"

    return NLPResult(
        original_text=user_input,
        normalized_text=corrected,
        clean_text=clean,
        tokens=tokens,
        intent=intent,
        confidence=round(float(confidence), 3),
        canonical_command=canonical_command,
        entities=entities,
        matched_phrase=matched_phrase,
        safety_level=safety_level,
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
    canonical = result.canonical_command or "None"
    matched = result.matched_phrase or "None"

    return f"""PHASE 000 NLP ENGINE REPORT

Original:
{result.original_text}

Normalized:
{result.normalized_text}

Clean routing text:
{result.clean_text}

Intent: {result.intent}
Confidence: {result.confidence}
Canonical command: {canonical}
Matched phrase: {matched}
Safety level: {result.safety_level}
Engine: {result.engine}

Entities:
{entities}

Tokens:
{', '.join(result.tokens) if result.tokens else 'None'}"""
