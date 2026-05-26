from pathlib import Path
import re

from tools.project_context_tools import get_current_project_path
from tools.invoice_ocr_tools import _extract_text

SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp", ".pdf"]
MAX_FILES = 25

RECEIPT_KEYWORDS = [
    "receipt",
    "bill",
    "payment",
    "purchase",
    "pos",
    "cash",
]


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected. Use: use project <name-or-path>"
    return Path(project), None


def _skip(path: Path):
    skip_dirs = {".git", "venv", "__pycache__", "node_modules", "vendor"}
    return any(part in skip_dirs for part in path.parts)


def _find_receipt_files(project: Path):
    files = []

    for ext in SUPPORTED_EXTENSIONS:
        for file in project.rglob(f"*{ext}"):
            if _skip(file) or not file.is_file():
                continue

            name = file.name.lower()
            if any(keyword in name for keyword in RECEIPT_KEYWORDS):
                files.append(file)

    return sorted(files)[:MAX_FILES]


def _first_match(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _money_values(text):
    pattern = r"(?:Rs\.?|LKR|USD|\$)?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.\d{2})?|[0-9]+(?:\.\d{2})?)"
    values = []

    for match in re.finditer(pattern, text):
        try:
            values.append(float(match.group(1).replace(",", "")))
        except ValueError:
            continue

    return values


def _parse_receipt_text(text):
    clean = " ".join(text.split())

    receipt_number = _first_match([
        r"receipt\s*(?:no|number|#)?\s*[:\-]?\s*([A-Z0-9\-\/]+)",
        r"bill\s*(?:no|number|#)?\s*[:\-]?\s*([A-Z0-9\-\/]+)",
        r"transaction\s*(?:id|no|number)?\s*[:\-]?\s*([A-Z0-9\-\/]+)",
    ], clean)

    date = _first_match([
        r"(?:date|paid on|purchase date)\s*[:\-]?\s*([0-9]{1,2}[\/\-.][0-9]{1,2}[\/\-.][0-9]{2,4})",
        r"([0-9]{4}[\/\-.][0-9]{1,2}[\/\-.][0-9]{1,2})",
    ], clean)

    payment_method = _first_match([
        r"(cash|card|visa|mastercard|bank transfer|online payment|qr payment)",
    ], clean)

    total = _first_match([
        r"(?:grand total|total paid|amount paid|net total|total)\s*[:\-]?\s*(?:Rs\.?|LKR|USD|\$)?\s*([0-9,]+(?:\.\d{2})?)",
    ], clean)

    values = _money_values(clean)

    return {
        "receipt_number": receipt_number,
        "date": date,
        "payment_method": payment_method,
        "total": total,
        "estimated_total": max(values) if values else None,
        "money_count": len(values),
    }


def receipt_parser():
    project, error = _project()
    if error:
        return error

    files = _find_receipt_files(project)

    lines = [
        "RECEIPT PARSER — PHASE 344",
        f"Project: {project}",
        "",
        "Mode: read-only receipt parsing.",
        "",
    ]

    if not files:
        lines.append("No receipt-like files found.")
        lines.append("")
        lines.append("File names should include words like:")
        lines.append("- receipt")
        lines.append("- bill")
        lines.append("- payment")
        lines.append("- purchase")
        lines.append("- pos")
        return "\n".join(lines)

    lines.append(f"Receipt-like files found: {len(files)}")
    lines.append("")

    for file in files:
        try:
            text = _extract_text(file)
            result = _parse_receipt_text(text)

            lines.append("=" * 80)
            lines.append(f"FILE: {file.relative_to(project)}")
            lines.append("=" * 80)
            lines.append(f"- Receipt number: {result['receipt_number'] or 'NOT DETECTED'}")
            lines.append(f"- Date: {result['date'] or 'NOT DETECTED'}")
            lines.append(f"- Payment method: {result['payment_method'] or 'NOT DETECTED'}")
            lines.append(f"- Total detected: {result['total'] or 'NOT DETECTED'}")

            if result["estimated_total"] is not None:
                lines.append(f"- Estimated highest amount: {result['estimated_total']:,.2f}")
            else:
                lines.append("- Estimated highest amount: NOT DETECTED")

            lines.append(f"- Money-like values found: {result['money_count']}")
            lines.append("")

        except Exception as e:
            lines.append("=" * 80)
            lines.append(f"FILE: {file.relative_to(project)}")
            lines.append("=" * 80)
            lines.append(f"- Receipt parsing failed: {e}")
            lines.append("")

    lines.append("Important:")
    lines.append("- This is a read-only parser.")
    lines.append("- No files were modified.")
    lines.append("- Review extracted values before accounting use.")

    return "\n".join(lines)
