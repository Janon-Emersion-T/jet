import re
from typing import Dict


def extract_advanced_entities(text: str) -> Dict[str, str]:
    entities = {}

    url = re.search(r"https?://[^\s]+", text)
    if url:
        entities["url"] = url.group(0).rstrip(".,)")

    email = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    if email:
        entities["email"] = email.group(0)

    file_path = re.search(
        r"([\w\-/\.]+\.(?:py|php|js|ts|jsx|tsx|md|txt|json|env|html|css|sql|blade\.php|yml|yaml|csv|xlsx|docx|pdf))",
        text,
    )
    if file_path:
        entities["file"] = file_path.group(1)

    phase = re.search(
        r"\b(?:phase|phases)\s*(\d{1,5})(?:\s*[-–to]+\s*(\d{1,5}))?\b",
        text,
    )
    if phase:
        entities["phase_start"] = phase.group(1)
        if phase.group(2):
            entities["phase_end"] = phase.group(2)

    repo = re.search(r"github\.com/([\w\-]+/[\w\-\.]+)", text)
    if repo:
        entities["github_repo"] = repo.group(1).replace(".git", "")

    quoted = re.findall(r'"([^"]+)"|' + r"'([^']+)'", text)
    if quoted:
        entities["quoted_text"] = quoted[0][0] or quoted[0][1]

    number = re.search(r"\b\d+(?:\.\d+)?\b", text)
    if number:
        entities["number"] = number.group(0)

    money = re.search(r"(?:rs\.?|lkr|usd|\$)\s?\d+(?:,\d{3})*(?:\.\d+)?", text)
    if money:
        entities["money"] = money.group(0)

    date_like = re.search(
        r"\b(?:today|tomorrow|yesterday|next week|this week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
        text,
    )
    if date_like:
        entities["date_reference"] = date_like.group(0)

    return entities
