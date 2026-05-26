import re
import string
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple


@dataclass
class FoundationNLPResult:
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
    engine: str = "nlp-000a-foundation"


INTENT_EXAMPLES = {
    "weather": ["weather", "rain", "temperature", "forecast"],
    "location": ["where am i", "my location", "current location"],
    "camera": ["camera", "see me", "scan room", "look around"],
    "email": ["email", "inbox", "send mail", "gmail"],
    "calendar": ["calendar", "schedule", "meeting", "appointment"],
    "browser_control": ["open google", "open youtube", "open github", "visit website", "launch browser"],
    "google_search": ["search google for", "google search", "search for", "look up"],
    "project_analysis": ["analyze project", "scan project", "project health", "inspect project", "check project"],
    "patch_workflow": ["apply patch", "file diff", "compare patch", "rollback proposal", "confirm before write"],
    "devops": ["git status", "deploy", "deployment", "server", "nginx", "logs", "disk cleanup"],
    "database": ["sql", "database", "migration", "schema", "n plus one", "n+1", "eloquent"],
    "content": ["blog ideas", "seo brief", "social post", "case study", "proposal", "quote"],
    "memory": ["remember", "save memory", "what do you remember", "forget"],
    "task": ["task", "todo", "remind", "deadline"],
    "nlp": ["nlp", "test nlp", "analyze command", "parse intent"],
}


CANONICAL_COMMANDS = {
    "capabilities": ["capabilities", "list capabilities", "what can you do"],
    "show current folder": ["show current folder", "where am i", "current directory", "pwd"],
    "list files": ["list files", "show files", "ls"],
    "show disk usage": ["show disk usage", "disk usage", "check disk"],
    "show memory usage": ["show memory usage", "memory usage", "ram usage"],
    "show date": ["show date", "date"],
    "who am i": ["who am i", "current user"],
    "python version": ["python version", "check python"],
    "node version": ["node version", "check node"],
    "npm version": ["npm version", "check npm"],
    "activate voice mode": ["activate voice mode", "start voice mode", "voice mode"],
}


TYPO_CORRECTIONS = {
    "jarwis": "jarvis",
    "jervis": "jarvis",
    "opne": "open",
    "serach": "search",
    "gogle": "google",
    "googl": "google",
    "yt": "youtube",
    "capabilites": "capabilities",
    "rember": "remember",
    "anlyze": "analyze",
    "analize": "analyze",
    "deployement": "deployment",
}


DANGEROUS_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bsudo\s+rm\b",
    r"\bmkfs\b",
    r"\bdd\s+if=",
    r"\bshutdown\s+now\b",
    r"\breboot\b",
    r"\bchmod\s+777\s+/\b",
    r"\bformat\s+disk\b",
]


def normalize_text(user_input: str) -> str:
    text = unicodedata.normalize("NFKC", user_input or "")
    text = text.replace("’", "'").replace("`", "'").replace("\u2014", "-")
    text = text.lower().strip()
    return re.sub(r"\s+", " ", text)


def correct_typos(text: str) -> str:
    words = []
    for word in text.split():
        stripped = word.strip(string.punctuation)
        replacement = TYPO_CORRECTIONS.get(stripped, stripped)
        words.append(word.replace(stripped, replacement))
    return " ".join(words)


def clean_for_routing(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation)).strip()


def tokenize(text: str) -> List[str]:
    return [word for word in clean_for_routing(text).split() if word]


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def detect_safety_level(text: str) -> str:
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, text):
            return "dangerous"

    if any(word in text for word in ["delete", "remove", "wipe", "format", "kill", "overwrite"]):
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

    phase_match = re.search(r"\b(?:phase|phases)\s*(\d{1,4})(?:\s*[-–]\s*(\d{1,4}))?\b", text)
    if phase_match:
        entities["phase_start"] = phase_match.group(1)
        if phase_match.group(2):
            entities["phase_end"] = phase_match.group(2)

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
            elif phrase_clean in clean_text:
                score = max(score, 0.88)

            if score > best_score:
                best_command = canonical
                best_score = score
                best_phrase = phrase

    if best_score >= 0.82:
        return best_command, best_score, best_phrase

    return None, 0.0, None


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


def analyze_foundation_command(user_input: str) -> FoundationNLPResult:
    normalized = normalize_text(user_input)
    corrected = correct_typos(normalized)
    clean = clean_for_routing(corrected)
    tokens = tokenize(corrected)

    canonical_command, canonical_score, canonical_phrase = detect_canonical_command(clean)
    intent, confidence, matched_phrase = classify_with_keywords(corrected, clean, tokens)

    if canonical_command and canonical_score >= max(confidence, 0.82):
        clean = canonical_command
        corrected = canonical_command
        intent = "command"
        confidence = canonical_score
        matched_phrase = canonical_phrase

    return FoundationNLPResult(
        original_text=user_input,
        normalized_text=corrected,
        clean_text=clean,
        tokens=tokens,
        intent=intent,
        confidence=round(float(confidence), 3),
        canonical_command=canonical_command,
        entities=extract_entities(corrected),
        matched_phrase=matched_phrase,
        safety_level=detect_safety_level(corrected),
    )
