from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class SQLInjectionFinding:
    language: str
    sink: str
    severity: str
    file: str
    line: int
    evidence: str
    recommendation: str


SQL_INJECTION_RULES: List[Tuple[str, str, str, Pattern[str], str]] = [
    (
        "Python DB-API",
        "Formatted SQL passed to execute",
        "high",
        re.compile(r"\bexecute(?:many)?\s*\(\s*(?:f[\"']|[^)\n]*?\.format\s*\(|[^)\n]*?(?:\+|%))"),
        "Use parameter placeholders and pass user-controlled values as query parameters.",
    ),
    (
        "Laravel/PHP",
        "Dynamic value in raw query API",
        "high",
        re.compile(
            r"(?:DB::(?:raw|select|statement)|->(?:whereRaw|orderByRaw|havingRaw))"
            r"\s*\([^;\n]*(?:\$|request\s*\(|input\s*\()",
            re.IGNORECASE,
        ),
        "Use query builder bindings or parameter arrays instead of constructing raw SQL.",
    ),
    (
        "PHP",
        "Dynamic value in query execution",
        "high",
        re.compile(r"(?:mysqli_query|->query)\s*\([^;\n]*\$", re.IGNORECASE),
        "Use prepared statements with bound parameters.",
    ),
    (
        "Node.js",
        "Template value in query execution",
        "high",
        re.compile(r"\b(?:query|execute)\s*\(\s*`[^`\n]*\$\{", re.IGNORECASE),
        "Use driver placeholders or named bindings for external values.",
    ),
    (
        "Node.js",
        "Concatenated SQL in query execution",
        "high",
        re.compile(r"\b(?:query|execute)\s*\([^;\n]*\+", re.IGNORECASE),
        "Use driver placeholders or named bindings for external values.",
    ),
]
EXTENSIONS = {".py", ".php", ".js", ".ts", ".jsx", ".tsx"}
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def _safe_evidence(line: str) -> str:
    evidence = line.strip()[:180]
    return re.sub(
        r"(?i)(password|secret|token)\s*=\s*([\"']).*?\2",
        r"\1=<redacted>",
        evidence,
    )


def detect_sql_injection_risks(
    project: Optional[Path] = None,
) -> Tuple[Optional[Path], List[SQLInjectionFinding], Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], "No current project selected. Use: use project <name-or-path>"

    findings: List[SQLInjectionFinding] = []
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file():
            continue
        if file.suffix.lower() not in EXTENSIONS:
            continue
        if file.name == "sql_injection_risk_tools.py" or file.name.startswith("test_"):
            continue
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines[:5000], start=1):
            for language, sink, severity, pattern, recommendation in SQL_INJECTION_RULES:
                if pattern.search(line):
                    findings.append(SQLInjectionFinding(
                        language,
                        sink,
                        severity,
                        str(file.relative_to(root)),
                        number,
                        _safe_evidence(line),
                        recommendation,
                    ))
    return Path(root), findings, None


def sql_injection_risk_detector(project: Optional[Path] = None) -> str:
    root, findings, error = detect_sql_injection_risks(project)
    if error:
        return error
    lines = [
        "SQL INJECTION RISK DETECTOR - PHASE 358",
        f"Project: {root}",
        "",
        "Mode: read-only dynamic SQL sink review.",
        f"Possible sinks: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.severity.upper()} {finding.language}: {finding.sink} | {finding.file}:{finding.line}",
            f"  Evidence: {finding.evidence}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if not findings:
        lines.append("No configured SQL injection sink indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- Findings identify review points; confirm data flow before treating them as exploitable.",
        "- No queries are executed and no source files are changed.",
    ])
    return "\n".join(lines)
