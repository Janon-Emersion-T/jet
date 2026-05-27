from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class CSRFFinding:
    category: str
    file: str
    detail: str
    recommendation: str


SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def analyze_csrf(project: Optional[Path] = None) -> Tuple[Optional[Path], List[CSRFFinding], Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], "No current project selected. Use: use project <name-or-path>"

    findings: List[CSRFFinding] = []
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file():
            continue
        if file.name == "csrf_analyzer_tools.py":
            continue
        name = file.name.lower()
        if not (
            name.endswith(".blade.php")
            or file.suffix.lower() in {".js", ".ts", ".jsx", ".tsx", ".php"}
        ):
            continue
        try:
            content = file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        relative = str(file.relative_to(root))

        if name.endswith(".blade.php"):
            state_form = re.search(r"(?is)<form[^>]*method\s*=\s*['\"](?:post|put|patch|delete)['\"]", content)
            if state_form and "@csrf" not in content:
                findings.append(CSRFFinding(
                    "Blade form missing CSRF token",
                    relative,
                    "State-changing form found without visible `@csrf`.",
                    "Add `@csrf` inside the form and retain server-side CSRF middleware.",
                ))

        if file.suffix.lower() in {".js", ".ts", ".jsx", ".tsx"}:
            request = re.search(
                r"(?is)(?:fetch\s*\(.{0,180}method\s*:\s*['\"](?:POST|PUT|PATCH|DELETE)['\"]"
                r"|axios\.(?:post|put|patch|delete)\s*\()",
                content,
            )
            token = re.search(r"(?i)(?:x-csrf-token|x-xsrf-token|csrf-token)", content)
            if request and not token:
                findings.append(CSRFFinding(
                    "Client request without visible CSRF header",
                    relative,
                    "State-changing browser request found without a nearby CSRF token/header reference.",
                    "Send the framework CSRF header/token for authenticated browser mutations.",
                ))

        if file.suffix.lower() == ".php" and re.search(r"(?i)verifycsrftoken|validatecsrftokens", content):
            if re.search(r"(?i)(?:except|exclude).{0,120}(?:\*|api|webhook)", content):
                findings.append(CSRFFinding(
                    "CSRF exclusion requires review",
                    relative,
                    "A CSRF exclusion pattern may cover state-changing endpoints.",
                    "Keep exceptions narrow and use signed/authenticated alternatives where CSRF does not apply.",
                ))

    return Path(root), findings, None


def csrf_analyzer(project: Optional[Path] = None) -> str:
    root, findings, error = analyze_csrf(project)
    if error:
        return error
    lines = [
        "CSRF ANALYZER - PHASE 357",
        f"Project: {root}",
        "",
        "Mode: read-only cross-site request forgery review.",
        f"Review points: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.category} | {finding.file}",
            f"  Detail: {finding.detail}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if not findings:
        lines.append("No configured CSRF review points detected.")
    lines.extend([
        "",
        "Safety:",
        "- Static heuristic analysis only; verify framework middleware and request flow manually.",
        "- No forms, routes, or middleware were modified.",
    ])
    return "\n".join(lines)
