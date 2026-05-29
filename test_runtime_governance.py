import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.runtime_governance_tools import (
    ai_driven_identity_governance,
    ai_policy_enforcement_engine,
    secure_execution_enclave,
    semantic_permission_layers,
)


class RuntimeGovernanceTests(unittest.TestCase):
    def test_runtime_governance_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "semantic_permissions.json").write_text(
                json.dumps(
                    {
                        "layers": [{"name": "operator", "trust": "privileged"}, {"name": "viewer", "trust": "standard"}],
                        "rules": [{"context_scoped": True}, {"context_scoped": False}],
                    }
                ),
                encoding="utf-8",
            )
            (root / "identity_governance.json").write_text(
                json.dumps(
                    {
                        "identities": [
                            {"name": "ada", "last_review_days": 12, "mfa_enforced": True},
                            {"name": "legacy-bot", "last_review_days": 180, "mfa_enforced": False},
                        ],
                        "policies": [{"name": "review-window"}, {"name": "break-glass"}],
                    }
                ),
                encoding="utf-8",
            )
            (root / "policy_enforcement.json").write_text(
                json.dumps(
                    {
                        "events": [{"decision": "blocked"}, {"decision": "allowed"}],
                        "controls": [{"auto_remediation": True}, {"auto_remediation": False}],
                    }
                ),
                encoding="utf-8",
            )
            (root / "execution_enclave.json").write_text(
                json.dumps(
                    {
                        "enclaves": [{"isolated": True}, {"isolated": False}],
                        "attestations": [{"status": "valid"}, {"status": "expired"}],
                    }
                ),
                encoding="utf-8",
            )
            with patch("tools.runtime_governance_tools.RUNTIME_SECURITY_DIR", root):
                permissions = semantic_permission_layers()
                identities = ai_driven_identity_governance()
                policy = ai_policy_enforcement_engine()
                enclave = secure_execution_enclave()
        self.assertIn("Permission layers: 2", permissions)
        self.assertIn("Privileged layers: 1", permissions)
        self.assertIn("Identities tracked: 2", identities)
        self.assertIn("Stale identities: 1", identities)
        self.assertIn("Blocked events: 1", policy)
        self.assertIn("Auto-remediating controls: 1", policy)
        self.assertIn("Enclaves tracked: 2", enclave)
        self.assertIn("Valid attestations: 1", enclave)

    def test_routes_cover_527_to_530(self):
        for phase in range(527, 531):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
