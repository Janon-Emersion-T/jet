from core.patches.proposal_manager import ProposalManager


class SafeWriter:
    def __init__(self, root="."):
        self.manager = ProposalManager(root=root)

    def propose_write(self, file_path, new_content, reason="AI proposed file update"):
        try:
            proposal = self.manager.create_proposal(file_path, new_content, reason)
            diff = self.manager.diff(proposal["id"])

            return {
                "status": "proposal_created",
                "proposal": proposal,
                "diff": diff,
                "message": "No file was changed. Review diff, then confirm apply.",
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Proposal creation failed: {e}",
            }

    def diff_proposal(self, proposal_id):
        try:
            return self.manager.diff(proposal_id)
        except Exception as e:
            return f"Diff failed: {e}"

    def compare_proposal(self, proposal_id):
        try:
            return self.manager.compare(proposal_id)
        except Exception as e:
            return {
                "error": True,
                "message": f"Compare failed: {e}",
            }

    def apply_proposal(self, proposal_id, confirm=False):
        try:
            return self.manager.apply(proposal_id, confirmed=confirm)
        except Exception as e:
            return f"Apply failed: {e}"

    def rollback_proposal(self, proposal_id):
        try:
            return self.manager.rollback(proposal_id)
        except Exception as e:
            return f"Rollback failed: {e}"

    def list_proposals(self):
        try:
            return self.manager.list_proposals()
        except Exception:
            return []