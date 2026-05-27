from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Dict, List, Optional


@dataclass
class KnowledgeContext:
    documentation: List[str] = field(default_factory=list)
    related_errors: List[str] = field(default_factory=list)
    symbols: List[str] = field(default_factory=list)
    route_handler: Optional[str] = None
    missing_capabilities: List[str] = field(default_factory=list)
    rag_snippets: List[str] = field(default_factory=list)


ROUTE_KEYWORDS = {
    "git": "dev_ops_routes",
    "deploy": "dev_ops_routes",
    "browser": "browser_routes",
    "database": "database_intelligence_routes",
    "laravel": "advanced_laravel_routes",
    "file": "project_context_routes",
    "memory": "memory_routes",
}
CAPABILITY_WORDS = {
    "email": "email",
    "calendar": "calendar",
    "camera": "camera",
    "weather": "weather",
}


def _root(project_root: Optional[str]) -> Path:
    return Path(project_root).resolve() if project_root else Path.cwd().resolve()


def _docs(root: Path, query: str) -> List[str]:
    terms = set(re.findall(r"[a-z]{4,}", query.lower()))
    snippets = []
    for path in list(root.glob("*.md"))[:12]:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")[:8000]
        except OSError:
            continue
        if not terms or any(term in content.lower() for term in terms):
            snippets.append(f"{path.name}: {content.splitlines()[0][:100] if content else 'empty'}")
    return snippets[:4]


def _symbols(root: Path, query: str) -> List[str]:
    names = set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_]{3,}\b", query))
    matches = []
    for path in list((root / "core").rglob("*.py"))[:150] if (root / "core").exists() else []:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name in names:
            if re.search(rf"\b(?:class|def)\s+{re.escape(name)}\b", content):
                matches.append(f"{name} ({path.relative_to(root)})")
    return matches[:8]


def build_knowledge_context(text: str, project_root: Optional[str] = None) -> KnowledgeContext:
    root = _root(project_root)
    lowered = text.lower()
    docs = _docs(root, text)
    error_file = root / "storage" / "events" / "events.log"
    errors = []
    if error_file.exists() and any(word in lowered for word in ["error", "failed", "fix"]):
        errors = error_file.read_text(encoding="utf-8", errors="ignore").splitlines()[-5:]
    handler = next((route for word, route in ROUTE_KEYWORDS.items() if word in lowered), None)
    missing = []
    try:
        from core.capabilities import CAPABILITIES

        missing = [
            capability for word, capability in CAPABILITY_WORDS.items()
            if word in lowered and CAPABILITIES.get(capability, {}).get("status") != "active"
        ]
    except Exception:
        pass
    return KnowledgeContext(
        documentation=docs,
        related_errors=errors,
        symbols=_symbols(root, text),
        route_handler=handler,
        missing_capabilities=missing,
        rag_snippets=docs + errors,
    )
