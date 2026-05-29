from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Optional, Pattern, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class FileUploadFinding:
    framework: str
    risk: str
    severity: str
    file: str
    line: int
    evidence: str
    recommendation: str


UPLOAD_RULES: List[Tuple[str, str, str, Pattern[str], str]] = [
    (
        "PHP",
        "Uploaded file moved into a public directory",
        "high",
        re.compile(r"\bmove_uploaded_file\s*\([^;\n]*(?:public|uploads?)", re.IGNORECASE),
        "Store uploads outside the web root and serve approved files through controlled downloads.",
    ),
    (
        "Laravel",
        "Upload stored directly in public location",
        "high",
        re.compile(r"(?:->move|->storeAs?)\s*\([^;\n]*(?:public_path|['\"]public|uploads?)", re.IGNORECASE),
        "Validate MIME/content, generate server-side names, and store outside public execution paths.",
    ),
    (
        "Express",
        "Multer writes uploads into public assets",
        "high",
        re.compile(r"\bmulter\s*\(\s*\{[^}\n]*dest\s*:\s*['\"][^'\"]*(?:public|uploads?)", re.IGNORECASE),
        "Use a quarantined upload directory and validate content before exposing files.",
    ),
    (
        "Upload validation",
        "Executable extension accepted for upload",
        "critical",
        re.compile(
            r"(?:allowed_extensions|mimes|extensions)[^;\n]*(?:php|phtml|phar|exe|sh|jsp|asp)",
            re.IGNORECASE,
        ),
        "Reject executable/script types and enforce an explicit content-based allowlist.",
    ),
]
EXTENSIONS = {".py", ".php", ".js", ".ts", ".jsx", ".tsx"}
SKIP = {".git", "node_modules", "vendor", "venv", "__pycache__", "storage", "dist", "build"}


def inspect_file_upload_security(
    project: Optional[Path] = None,
) -> Tuple[Optional[Path], List[FileUploadFinding], Optional[str]]:
    root = Path(project).resolve() if project else get_current_project_path()
    if not root:
        return None, [], "No current project selected. Use: use project <name-or-path>"

    findings: List[FileUploadFinding] = []
    for file in Path(root).rglob("*"):
        if any(part in SKIP for part in file.parts) or not file.is_file():
            continue
        if file.suffix.lower() not in EXTENSIONS or file.name.startswith("test_"):
            continue
        if file.name == "file_upload_security_tools.py":
            continue
        try:
            lines = file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines[:5000], start=1):
            for framework, risk, severity, pattern, recommendation in UPLOAD_RULES:
                if pattern.search(line):
                    findings.append(FileUploadFinding(
                        framework,
                        risk,
                        severity,
                        str(file.relative_to(root)),
                        number,
                        line.strip()[:180],
                        recommendation,
                    ))
    return Path(root), findings, None


def file_upload_security_checker(project: Optional[Path] = None) -> str:
    root, findings, error = inspect_file_upload_security(project)
    if error:
        return error
    lines = [
        "FILE UPLOAD SECURITY CHECKER - PHASE 360",
        f"Project: {root}",
        "",
        "Mode: read-only file upload handling review.",
        f"Review points: {len(findings)}",
        "",
    ]
    for finding in findings[:80]:
        lines.extend([
            f"- {finding.severity.upper()} {finding.framework}: {finding.risk} | {finding.file}:{finding.line}",
            f"  Evidence: {finding.evidence}",
            f"  Recommendation: {finding.recommendation}",
        ])
    if not findings:
        lines.append("No configured unsafe file upload indicators detected.")
    lines.extend([
        "",
        "Safety:",
        "- Static indicators do not upload, open, or execute any files.",
        "- Confirm server-side validation, filename generation, and storage permissions manually.",
    ])
    return "\n".join(lines)
