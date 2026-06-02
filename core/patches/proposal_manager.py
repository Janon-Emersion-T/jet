from pathlib import Path
from datetime import datetime
import json
import shutil
import difflib
import uuid
from tools.event_tools import emit_event


class ProposalManager:
    def __init__(self, root="."):
        self.root = Path(root).resolve()
        self.store = self.root / ".jarvis_proposals"
        self.store.mkdir(exist_ok=True)

    def _safe_path(self, file_path):
        target = (self.root / file_path).resolve()
        if not str(target).startswith(str(self.root)):
            raise ValueError("Blocked unsafe path access.")
        return target

    def _folder(self, proposal_id):
        folder = self.store / proposal_id
        if not folder.exists():
            raise FileNotFoundError(f"Proposal not found: {proposal_id}")
        return folder

    def create_proposal(self, file_path, new_content, reason="AI proposed change"):
        target = self._safe_path(file_path)
        proposal_id = str(uuid.uuid4())[:8]
        folder = self.store / proposal_id
        folder.mkdir()

        old_content = target.read_text(encoding="utf-8") if target.exists() else ""

        (folder / "old.txt").write_text(old_content, encoding="utf-8")
        (folder / "new.txt").write_text(new_content, encoding="utf-8")

        meta = {
            "id": proposal_id,
            "file_path": str(file_path),
            "reason": reason,
            "created_at": datetime.now().isoformat(),
            "applied": False,
            "rolled_back": False,
            "confirm_before_write": True,
        }

        (folder / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return meta

    def diff(self, proposal_id):
        folder = self._folder(proposal_id)
        meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))

        old = (folder / "old.txt").read_text(encoding="utf-8").splitlines()
        new = (folder / "new.txt").read_text(encoding="utf-8").splitlines()

        return "\n".join(difflib.unified_diff(
            old,
            new,
            fromfile=f"OLD: {meta['file_path']}",
            tofile=f"NEW: {meta['file_path']}",
            lineterm=""
        ))

    def compare(self, proposal_id):
        folder = self._folder(proposal_id)
        old = (folder / "old.txt").read_text(encoding="utf-8")
        new = (folder / "new.txt").read_text(encoding="utf-8")

        return {
            "old": old,
            "new": new,
            "diff": self.diff(proposal_id),
        }

    def apply(self, proposal_id, confirmed=False):
        folder = self._folder(proposal_id)
        meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))

        if not confirmed:
            return (
                "Write blocked.\n"
                "Confirm-before-write mode is active.\n"
                f"Use: confirm apply proposal {proposal_id}"
            )

        if meta.get("applied") and not meta.get("rolled_back"):
            return f"Proposal {proposal_id} is already applied."

        target = self._safe_path(meta["file_path"])
        backup = folder / "backup.txt"

        if target.exists():
            shutil.copyfile(target, backup)
        else:
            backup.write_text("", encoding="utf-8")

        new_content = (folder / "new.txt").read_text(encoding="utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_content, encoding="utf-8")

        meta["applied"] = True
        meta["rolled_back"] = False
        meta["applied_at"] = datetime.now().isoformat()

        (folder / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        emit_event(
            "PATCH_APPLIED",
            "Safe patch applied",
            f"Proposal {proposal_id} applied to {meta['file_path']}",
        )

        return f"Applied proposal {proposal_id} to {meta['file_path']}"

    def rollback(self, proposal_id):
        folder = self._folder(proposal_id)
        meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))

        target = self._safe_path(meta["file_path"])
        backup = folder / "backup.txt"
        old = folder / "old.txt"

        if backup.exists():
            restore_content = backup.read_text(encoding="utf-8")
        elif old.exists():
            restore_content = old.read_text(encoding="utf-8")
        else:
            return "Rollback failed. No backup or old content found."

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(restore_content, encoding="utf-8")

        meta["rolled_back"] = True
        meta["rolled_back_at"] = datetime.now().isoformat()

        (folder / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        emit_event(
            "PATCH_ROLLED_BACK",
            "Patch rollback completed",
            f"Proposal {proposal_id} rolled back on {meta['file_path']}",
        )

        return f"Rolled back proposal {proposal_id} on {meta['file_path']}"

    def list_proposals(self):
        proposals = []

        for folder in self.store.iterdir():
            meta_file = folder / "meta.json"
            if meta_file.exists():
                proposals.append(json.loads(meta_file.read_text(encoding="utf-8")))

        return sorted(proposals, key=lambda x: x.get("created_at", ""), reverse=True)
