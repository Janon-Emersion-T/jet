from dataclasses import dataclass, field
import re
from typing import Dict, List, Optional

from core.nlp.file_awareness import understand_file_command


@dataclass
class ResolvedTargets:
    file: Optional[str] = None
    git: Optional[str] = None
    laravel: Optional[str] = None
    server: Optional[str] = None
    database: Optional[str] = None
    browser: Optional[str] = None
    matches: Dict[str, List[str]] = field(default_factory=dict)


def _first(patterns: List[str], text: str) -> Optional[str]:
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group(1) if match.groups() else match.group(0)
    return None


def resolve_targets(text: str, entities: Optional[Dict[str, str]] = None) -> ResolvedTargets:
    lowered = text or ""
    files = understand_file_command(lowered, entities)
    git = _first([
        r"github\.com/([\w.-]+/[\w.-]+)",
        r"\b(?:branch|checkout|merge|rebase)\s+([\w./-]+)",
        r"\b(?:commit|pr|pull request)\s+#?(\d+)",
    ], lowered)
    laravel = _first([
        r"\b(?:controller|model|middleware|migration|route|blade view)\s+([\w\\/.-]+)",
        r"\b(artisan|eloquent|laravel)\b",
    ], lowered)
    server = _first([
        r"\b(?:server|host|ssh|nginx|service)\s+([\w.-]+)",
        r"\b(nginx|apache|php-fpm|docker)\b",
    ], lowered)
    database = _first([
        r"\b(?:database|db|schema|table)\s+[`'\"]?([\w.-]+)",
        r"\b(mysql|postgres(?:ql)?|sqlite|redis)\b",
    ], lowered)
    browser = (entities or {}).get("url") or _first([
        r"(https?://[^\s]+)", r"\b(?:open|visit|browse)\s+([\w.-]+\.[a-z]{2,})",
    ], lowered)
    return ResolvedTargets(
        file=files.primary_target,
        git=git,
        laravel=laravel,
        server=server,
        database=database,
        browser=browser,
        matches={
            "files": [target.resolved_path for target in files.targets],
        },
    )
