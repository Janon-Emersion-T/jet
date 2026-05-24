from pathlib import Path
from datetime import datetime
import json
import shutil
import difflib
import uuid


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
        }

        (folder / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return meta

    def diff(self, proposal_id):
        folder = self.store / proposal_id
        meta = json.loads((folder / "meta.json").read_text())

        old = (folder / "old.txt").read_text(encoding="utf-8").splitlines()
        new = (folder / "new.txt").read_text(encoding="utf-8").splitlines()

        return "\n".join(difflib.unified_diff(
            old,
            new,
            fromfile=f"OLD: {meta['file_path']}",
            tofile=f"NEW: {meta['file_path']}",
            lineterm=""
        ))

    def apply(self, proposal_id, confirmed=False):
        if not confirmed:
            return "Write blocked. Confirm-before-write mode requires confirmed=True."

        folder = self.store / proposal_id
        meta = json.loads((folder / "meta.json").read_text())

        target = self._safe_path(meta["file_path"])
        backup = folder / "backup.txt"

        if target.exists():
            shutil.copyfile(target, backup)

        new_content = (folder / "new.txt").read_text(encoding="utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(new_content, encoding="utf-8")

        meta["applied"] = True
        meta["applied_at"] = datetime.now().isoformat()
        (folder / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        return f"Applied proposal {proposal_id} to {meta['file_path']}"

    def rollback(self, proposal_id):
        folder = self.store / proposal_id
        meta = json.loads((folder / "meta.json").read_text())

        target = self._safe_path(meta["file_path"])
        backup = folder / "backup.txt"

        if not backup.exists():
            old = folder / "old.txt"
            if not old.exists():
                return "Rollback failed. No backup found."

            target.write_text(old.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            shutil.copyfile(backup, target)

        meta["rolled_back"] = True
        meta["rolled_back_at"] = datetime.now().isoformat()
        (folder / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        return f"Rolled back proposal {proposal_id} on {meta['file_path']}"

    def list_proposals(self):
        proposals = []

        for folder in self.store.iterdir():
            meta_file = folder / "meta.json"
            if meta_file.exists():
                proposals.append(json.loads(meta_file.read_text()))

        return proposals