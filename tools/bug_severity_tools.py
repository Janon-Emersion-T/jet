from pathlib import Path

from tools.project_context_tools import get_current_project_path

BUG_FILE_EXTENSIONS = [".py", ".js", ".ts", ".php", ".blade.php", ".vue", ".jsx", ".tsx", ".md", ".txt", ".log"]
MAX_FILES = 250
MAX_LINES_PER_FILE = 3000

SEVERITY_RULES = {
    "CRITICAL": [
        "sql injection",
        "remote code execution",
        "rce",
        "hardcoded password",
        "hardcoded secret",
        "private key",
        "api key",
        "token exposed",
        "eval(",
        "exec(",
        "shell_exec",
        "system(",
        "subprocess",
        "delete without confirmation",
        "drop table",
        "truncate table",
        "chmod 777",
    ],
    "HIGH": [
        "permission denied",
        "unauthorized",
        "forbidden",
        "authentication failed",
        "csrf",
        "xss",
        "missing validation",
        "file upload",
        "payment failed",
        "data loss",
        "production down",
        "500 error",
        "fatal error",
        "uncaught exception",
    ],
    "MEDIUM": [
        "bug",
        "broken",
        "not working",
        "failed",
        "error",
        "exception",
        "warning",
        "deprecated",
        "timeout",
        "slow query",
        "n+1",
        "null reference",
        "undefined variable",
        "undefined index",
    ],
    "LOW": [
        "typo",
        "minor",
        "ui issue",
        "alignment",
        "spacing",
        "cosmetic",
        "style issue",
        "improvement",
        "refactor",
    ],
}


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected. Use: use project <name-or-path>"
    return Path(project), None


def _skip(path: Path):
    skip_dirs = {
        ".git",
        "venv",
        "__pycache__",
        "node_modules",
        "vendor",
        "storage/reports",
        "storage/presentations",
        "storage/exports",
        "dist",
        "build",
    }
    return any(part in skip_dirs for part in path.parts)


def _read_text(file: Path):
    try:
        return file.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []


def _classify_line(line: str):
    lowered = line.lower()

    for severity, terms in SEVERITY_RULES.items():
        for term in terms:
            if term in lowered:
                return severity, term

    return None, None


def _severity_weight(severity: str):
    weights = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }
    return weights.get(severity, 0)


def bug_severity_classifier():
    project, error = _project()
    if error:
        return error

    findings = []
    scanned_files = 0

    for file in project.rglob("*"):
        if scanned_files >= MAX_FILES:
            break

        if _skip(file) or not file.is_file():
            continue

        name = file.name.lower()
        suffix = file.suffix.lower()

        if not any(name.endswith(ext) or suffix == ext for ext in BUG_FILE_EXTENSIONS):
            continue

        scanned_files += 1
        lines = _read_text(file)

        for line_number, line in enumerate(lines[:MAX_LINES_PER_FILE], start=1):
            severity, matched_term = _classify_line(line)
            if not severity:
                continue

            findings.append({
                "severity": severity,
                "term": matched_term,
                "file": str(file.relative_to(project)),
                "line": line_number,
                "text": line.strip()[:180],
            })

    findings.sort(key=lambda item: _severity_weight(item["severity"]), reverse=True)

    output = [
        "BUG SEVERITY CLASSIFIER — PHASE 352",
        f"Project: {project}",
        "",
        "Mode: read-only bug and risk classification.",
        "",
        f"Files scanned: {scanned_files}",
        f"Findings detected: {len(findings)}",
        "",
    ]

    if not findings:
        output.append("No obvious bug severity indicators detected.")
        output.append("")
        output.append("Safety:")
        output.append("- Read-only scan only.")
        output.append("- No files were modified.")
        return "\n".join(output)

    counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for finding in findings:
        counts[finding["severity"]] += 1

    output.append("SUMMARY")
    output.append(f"- Critical: {counts['CRITICAL']}")
    output.append(f"- High: {counts['HIGH']}")
    output.append(f"- Medium: {counts['MEDIUM']}")
    output.append(f"- Low: {counts['LOW']}")
    output.append("")
    output.append("TOP FINDINGS")
    output.append("")

    for index, finding in enumerate(findings[:40], start=1):
        output.append(f"{index}. {finding['severity']} | matched: {finding['term']}")
        output.append(f"   File: {finding['file']}:{finding['line']}")
        output.append(f"   Line: {finding['text']}")
        output.append("")

    output.append("Severity model:")
    output.append("- Critical: security, destructive actions, secrets, command execution.")
    output.append("- High: auth, validation, production, payment, fatal runtime risks.")
    output.append("- Medium: common bugs, exceptions, warnings, performance issues.")
    output.append("- Low: cosmetic, typo, refactor, minor UI issues.")
    output.append("")
    output.append("Safety:")
    output.append("- Read-only scan only.")
    output.append("- No files were modified.")

    return "\n".join(output)
