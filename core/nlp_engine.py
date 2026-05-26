from core.nlp.phase000_engine import analyze_command, classify_intent_nlp, format_nlp_report

import re
import string
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher, get_close_matches
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


FILLER_WORDS = {
    "please", "pls", "kindly", "jarvis", "hey", "hi", "hello", "can", "you",
    "could", "would", "me", "my", "the", "a", "an", "to", "for", "now"
}


TYPO_CORRECTIONS = {
    "jarwis": "jarvis",
    "jervis": "jarvis",
    "javris": "jarvis",
    "opne": "open",
    "serach": "search",
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


INTENT_PATTERNS = {
    "weather": ["weather", "rain", "temperature", "forecast"],
    "location": ["where am i", "my location", "which country", "current location"],
    "camera": ["camera", "see me", "look around", "scan room"],
    "email": ["email", "inbox", "send mail", "gmail"],
    "calendar": ["calendar", "schedule", "meeting", "appointment"],
    "browser_control": ["open google", "open website", "browser", "visit website", "open youtube", "open github", "open gmail"],
    "google_search": ["search google for", "google search", "search for", "look up", "find online"],
    "project_analysis": ["analyze project", "scan project", "project health", "inspect project", "check project"],
    "patch_workflow": ["apply patch", "proposal rollback", "file diff", "confirm before write", "patch comparison"],
    "devops": ["git status", "deploy", "deployment", "server", "nginx", "php fpm", "logs", "disk cleanup"],
    "database": ["sql", "database", "migration", "schema", "index suggestion", "n+1", "eloquent"],
    "content": ["blog ideas", "seo brief", "social post", "case study", "proposal", "quote"],
    "memory": ["remember", "save memory", "what do you remember", "forget"],
    "task": ["task", "todo", "remind", "deadline"],
    "nlp": ["nlp", "understand", "intent", "parse command", "analyze command"],
}


CANONICAL_COMMANDS = {
    "capabilities": ["capabilities", "list capabilities", "what can you do", "show abilities"],
    "show current folder": ["show current folder", "where am i", "current directory", "pwd"],
    "list files": ["list files", "show files", "ls", "show directory files"],
    "show disk usage": ["show disk usage", "disk usage", "check disk", "storage usage"],
    "show memory usage": ["show memory usage", "memory usage", "ram usage", "check memory"],
    "show date": ["show date", "date", "today date"],
    "who am i": ["who am i", "current user"],
    "python version": ["python version", "check python", "python --version"],
    "node version": ["node version", "check node", "node --version"],
    "npm version": ["npm version", "check npm", "npm --version"],
    "activate voice mode": ["activate voice mode", "start voice mode", "voice mode"],
}


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


def tokenize(text: str) -> List[str]:
    clean = clean_for_routing(text)
    return [
        word for word in clean.split()
        if word and word not in FILLER_WORDS
    ]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def detect_safety_level(text: str) -> str:
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, text):
            return "dangerous"

    destructive_words = ["delete", "remove", "wipe", "format", "kill", "terminate", "overwrite"]

    if any(word in text for word in destructive_words):
        return "needs_confirmation"

    return "safe"


def extract_entities(text: str) -> Dict[str, str]:
    entities = {}

    url_match = re.search(r"https?://\S+", text)
    if url_match:
        entities["url"] = url_match.group(0).rstrip(".,)")

    file_match = re.search(
        r"([\w\-/]+\.(?:py|php|js|ts|jsx|tsx|md|txt|json|env|html|css|sql))",
        text
    )
    if file_match:
        entities["file"] = file_match.group(1)

    phase_match = re.search(
        r"\b(?:phase|phases)\s*(\d{1,4})(?:\s*[-–]\s*(\d{1,4}))?\b",
        text
    )
    if phase_match:
        entities["phase_start"] = phase_match.group(1)
        if phase_match.group(2):
            entities["phase_end"] = phase_match.group(2)

    quoted_match = re.search(r"['\"]([^'\"]+)['\"]", text)
    if quoted_match:
        entities["quoted_text"] = quoted_match.group(1)

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

    all_phrases = [phrase for phrases in CANONICAL_COMMANDS.values() for phrase in phrases]
    matches = get_close_matches(clean_text, all_phrases, n=1, cutoff=0.82)

    if matches:
        match = matches[0]
        for canonical, phrases in CANONICAL_COMMANDS.items():
            if match in phrases:
                return canonical, similarity(clean_text, clean_for_routing(match)), match

    return None, 0.0, None


def classify_from_patterns(normalized_text: str, clean_text: str, tokens: List[str]) -> Tuple[str, float, Optional[str]]:
    best_intent = "general"
    best_score = 0.0
    best_phrase = None
    token_set = set(tokens)

    for intent, phrases in INTENT_PATTERNS.items():
        for phrase in phrases:
            phrase_clean = clean_for_routing(phrase)
            phrase_tokens = set(phrase_clean.split())

            if phrase in normalized_text or phrase_clean in clean_text:
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
    intent, intent_score, matched_phrase = classify_from_patterns(corrected, clean, tokens)

    if canonical_command and canonical_score >= max(intent_score, 0.82):
        clean = canonical_command
        corrected = canonical_command
        intent = "command"
        intent_score = canonical_score
        matched_phrase = canonical_phrase

    return NLPResult(
        original_text=user_input,
        normalized_text=corrected,
        clean_text=clean,
        tokens=tokens,
        intent=intent,
        confidence=round(float(intent_score), 3),
        canonical_command=canonical_command,
        entities=entities,
        matched_phrase=matched_phrase,
        safety_level=safety_level,
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

Entities:
{entities}

Tokens:
{', '.join(result.tokens) if result.tokens else 'None'}"""
