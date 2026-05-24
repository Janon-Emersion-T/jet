from pathlib import Path
import difflib


def view_file_diff(file_path, proposed_content):
    path = Path(file_path)

    old_content = path.read_text(encoding="utf-8") if path.exists() else ""

    old_lines = old_content.splitlines()
    new_lines = proposed_content.splitlines()

    return "\n".join(difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"CURRENT: {file_path}",
        tofile=f"PROPOSED: {file_path}",
        lineterm=""
    ))