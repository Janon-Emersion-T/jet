from pathlib import Path
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    REPORTLAB_AVAILABLE = True
except Exception:
    A4 = None
    getSampleStyleSheet = None
    SimpleDocTemplate = Paragraph = Spacer = None
    REPORTLAB_AVAILABLE = False

from tools.project_context_tools import get_current_project_path
from tools.project_health_tools import (
    project_todo_scanner,
    code_smell_detector,
    dead_file_detector,
    missing_import_detector,
    missing_route_detector,
    missing_view_detector,
    missing_component_detector,
    db_config_checker,
)


REPORT_DIR = Path("storage/reports")


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected. Use: use project <name-or-path>"
    return Path(project), None


def _safe_text(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )


def export_project_health_pdf():
    if not REPORTLAB_AVAILABLE:
        return "PDF export dependency missing. Install reportlab to enable PDF report export."

    project, error = _project()
    if error:
        return error

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project.name}_health_report_{timestamp}.pdf"
    output_path = REPORT_DIR / filename

    checks = [
        project_todo_scanner,
        code_smell_detector,
        dead_file_detector,
        missing_import_detector,
        missing_route_detector,
        missing_view_detector,
        missing_component_detector,
        db_config_checker,
    ]

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("JARVIS PROJECT HEALTH REPORT", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Project: {_safe_text(str(project))}", styles["Normal"]))
    story.append(Paragraph(f"Generated: {datetime.now().isoformat(timespec='seconds')}", styles["Normal"]))
    story.append(Spacer(1, 18))

    for check in checks:
        result = check()
        lines = result.splitlines()
        title = lines[0] if lines else check.__name__

        story.append(Paragraph(_safe_text(title), styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(_safe_text(result), styles["BodyText"]))
        story.append(Spacer(1, 14))

    doc.build(story)

    return f"""PDF REPORT EXPORTER — PHASE 338

Report generated successfully.

Project:
{project}

PDF file:
{output_path}

Safety:
- Read-only project inspection
- PDF written only inside storage/reports
- No project files were modified
"""
