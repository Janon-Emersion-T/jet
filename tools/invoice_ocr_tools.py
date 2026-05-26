from pathlib import Path
import re

from tools.project_context_tools import get_current_project_path

SUPPORTED_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp", ".pdf"]
MAX_FILES = 25
MAX_OUTPUT_CHARS = 12000

INVOICE_KEYWORDS = [
    "invoice",
    "bill",
    "receipt",
    "payment",
    "tax",
    "vat",
    "total",
    "amount",
]


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
    }
    return any(part in skip_dirs for part in path.parts)


def _find_invoice_files(project: Path):
    files = []

    for ext in SUPPORTED_EXTENSIONS:
        for file in project.rglob(f"*{ext}"):
            if _skip(file) or not file.is_file():
                continue

            name = file.name.lower()
            if any(keyword in name for keyword in INVOICE_KEYWORDS):
                files.append(file)

    return sorted(files)[:MAX_FILES]


def _extract_image_text(file: Path):
    try:
        from PIL import Image
        import pytesseract
    except Exception:
        raise ImportError("pillow-pytesseract")

    image = Image.open(file)
    return pytesseract.image_to_string(image)


def _extract_pdf_text(file: Path):
    try:
        import PyPDF2
    except Exception:
        raise ImportError("PyPDF2")

    blocks = []

    with file.open("rb") as handle:
        reader = PyPDF2.PdfReader(handle)
        for page_number, page in enumerate(reader.pages[:5], start=1):
            text = page.extract_text() or ""
            if text.strip():
                blocks.append(f"--- PAGE {page_number} ---\n{text.strip()}")

    return "\n\n".join(blocks)


def _extract_text(file: Path):
    if file.suffix.lower() == ".pdf":
        return _extract_pdf_text(file)

    return _extract_image_text(file)


def _first_match(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _money_values(text):
    pattern = r"(?:Rs\.?|LKR|USD|\$)?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.\d{2})?|[0-9]+(?:\.\d{2})?)"
    values = []

    for match in re.finditer(pattern, text, re.IGNORECASE):
        raw = match.group(1).replace(",", "")
        try:
            values.append(float(raw))
        except ValueError:
            continue

    return values


def _analyze_invoice_text(text):
    clean = " ".join(text.split())

    invoice_number = _first_match([
        r"invoice\s*(?:no|number|#)?\s*[:\-]?\s*([A-Z0-9\-\/]+)",
        r"bill\s*(?:no|number|#)?\s*[:\-]?\s*([A-Z0-9\-\/]+)",
        r"receipt\s*(?:no|number|#)?\s*[:\-]?\s*([A-Z0-9\-\/]+)",
    ], clean)

    date = _first_match([
        r"(?:invoice\s*)?date\s*[:\-]?\s*([0-9]{1,2}[\/\-.][0-9]{1,2}[\/\-.][0-9]{2,4})",
        r"([0-9]{4}[\/\-.][0-9]{1,2}[\/\-.][0-9]{1,2})",
    ], clean)

    tax_number = _first_match([
        r"(?:vat|tax)\s*(?:no|number|registration)?\s*[:\-]?\s*([A-Z0-9\-\/]+)",
    ], clean)

    total = _first_match([
        r"(?:grand\s+total|invoice\s+total|total\s+amount|amount\s+due|balance\s+due|total)\s*[:\-]?\s*(?:Rs\.?|LKR|USD|\$)?\s*([0-9,]+(?:\.\d{2})?)",
    ], clean)

    money_values = _money_values(clean)
    estimated_total = max(money_values) if money_values else None

    return {
        "invoice_number": invoice_number,
        "date": date,
        "tax_number": tax_number,
        "total": total,
        "estimated_total": estimated_total,
        "money_count": len(money_values),
    }


def _format_invoice_result(file: Path, project: Path, text: str):
    limited_text = text.strip()[:MAX_OUTPUT_CHARS]
    analysis = _analyze_invoice_text(text)

    lines = [
        "=" * 80,
        f"FILE: {file.relative_to(project)}",
        "=" * 80,
        f"- Invoice number: {analysis['invoice_number'] or 'NOT DETECTED'}",
        f"- Date: {analysis['date'] or 'NOT DETECTED'}",
        f"- Tax/VAT number: {analysis['tax_number'] or 'NOT DETECTED'}",
        f"- Total detected: {analysis['total'] or 'NOT DETECTED'}",
        f"- Estimated highest amount: {analysis['estimated_total']:,.2f}" if analysis["estimated_total"] is not None else "- Estimated highest amount: NOT DETECTED",
        f"- Money-like values found: {analysis['money_count']}",
        "",
        "OCR TEXT PREVIEW:",
        limited_text if limited_text else "No readable text detected.",
        "",
    ]

    return lines


def invoice_ocr_assistant():
    project, error = _project()
    if error:
        return error

    files = _find_invoice_files(project)

    lines = [
        "INVOICE OCR ASSISTANT — PHASE 343",
        f"Project: {project}",
        "",
        "Mode: read-only invoice OCR and extraction.",
        "",
    ]

    if not files:
        lines.append("No invoice-like image or PDF files found.")
        lines.append("")
        lines.append("File names should include words like:")
        lines.append("- invoice")
        lines.append("- bill")
        lines.append("- receipt")
        lines.append("- payment")
        return "\n".join(lines)

    lines.append(f"Invoice-like files found: {len(files)}")
    lines.append("")

    for file in files:
        try:
            text = _extract_text(file)
            lines.extend(_format_invoice_result(file, project, text))
        except ImportError as e:
            if str(e) == "PyPDF2":
                lines.append("PyPDF2 is required for PDF invoices.")
                lines.append("Install with: pip install PyPDF2")
            else:
                lines.append("Image OCR dependencies are required.")
                lines.append("Install with: pip install pillow pytesseract")
                lines.append("System package: sudo apt install tesseract-ocr -y")
            break
        except Exception as e:
            lines.append("=" * 80)
            lines.append(f"FILE: {file.relative_to(project)}")
            lines.append("=" * 80)
            lines.append(f"- OCR failed: {e}")
            lines.append("")

    lines.append("Important:")
    lines.append("- This is read-only.")
    lines.append("- No files were modified.")
    lines.append("- OCR results must be reviewed before accounting use.")

    return "\n".join(lines)
