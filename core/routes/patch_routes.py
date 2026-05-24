from core.patch_proposer import propose_patch
from core.patches.safe_writer import SafeWriter


def handle_patch_routes(user_input: str, text: str, clean_text: str):
    if text.startswith("propose patch "):
        command = user_input.replace("propose patch ", "", 1).strip()

        if ":::" not in command:
            return "Invalid format. Use: propose patch /path/to/file.py ::: instruction"

        target_file, instruction = command.split(":::", 1)
        return propose_patch(target_file.strip(), instruction.strip())

    if text in ["list proposals", "show proposals"]:
        writer = SafeWriter(root=".")
        proposals = writer.list_proposals()

        if not proposals:
            return "No proposals found."

        lines = ["Stored proposals:"]
        for p in proposals:
            status = "rolled_back" if p.get("rolled_back") else "applied" if p.get("applied") else "pending"
            lines.append(
                f"- {p['id']} | {status} | {p['file_path']} | {p.get('reason', 'No reason')}"
            )

        return "\n".join(lines)

    if text.startswith("diff proposal "):
        proposal_id = user_input.replace("diff proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        return writer.diff_proposal(proposal_id)

    if text.startswith("compare proposal "):
        proposal_id = user_input.replace("compare proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        comparison = writer.compare_proposal(proposal_id)

        if isinstance(comparison, dict) and comparison.get("error"):
            return comparison["message"]

        return (
            "PATCH COMPARISON MODE\n\n"
            "===== OLD FILE =====\n"
            f"{comparison['old']}\n\n"
            "===== NEW FILE =====\n"
            f"{comparison['new']}\n\n"
            "===== DIFF =====\n"
            f"{comparison['diff']}"
        )

    if text.startswith("apply proposal "):
        proposal_id = user_input.replace("apply proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        return writer.apply_proposal(proposal_id, confirm=False)

    if text.startswith("confirm apply proposal "):
        proposal_id = user_input.replace("confirm apply proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        return writer.apply_proposal(proposal_id, confirm=True)

    if text.startswith("rollback proposal "):
        proposal_id = user_input.replace("rollback proposal ", "", 1).strip()
        writer = SafeWriter(root=".")
        return writer.rollback_proposal(proposal_id)

    return None
