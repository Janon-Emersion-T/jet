from core.patches.proposal_manager import ProposalManager


class SafeWriter:
    def __init__(self, root="."):
        self.manager = ProposalManager(root=root)
        self.confirm_before_write = True

    def propose_write(self, file_path, new_content, reason="AI proposed file update"):
        proposal = self.manager.create_proposal(file_path, new_content, reason)
        diff = self.manager.diff(proposal["id"])

        return {
            "status": "proposal_created",
            "proposal": proposal,
            "diff": diff,
            "message": "No file was changed. Review diff, then approve apply."
        }

    def apply_proposal(self, proposal_id, confirm=False):
        return self.manager.apply(proposal_id, confirmed=confirm)

    def rollback_proposal(self, proposal_id):
        return self.manager.rollback(proposal_id)

    def list_proposals(self):
        return self.manager.list_proposals()