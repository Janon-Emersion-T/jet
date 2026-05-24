from pathlib import Path
from tools.system_tools import read_project_file, write_project_file

def apply_proposal(proposal_path: str) -> str:
    proposal = Path(proposal_path).expanduser()

    if not proposal.exists():
        return "Proposal file not found."

    if ".proposal-" not in str(proposal):
        return "Blocked. Only proposal files can be applied."

    original_path = str(proposal).split(".proposal-", 1)[0]

    content = read_project_file(str(proposal))

    if content.startswith("Blocked") or content.startswith("File not found"):
        return content

    if "\n\n" in content:
        content = content.split("\n\n", 1)[1]

    return write_project_file(original_path, content)