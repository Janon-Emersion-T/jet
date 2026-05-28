import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.compliance_governance_tools import (
    ai_legal_reasoning_layer,
    ai_policy_drafting_engine,
    enterprise_governance_framework,
    gdpr_readiness_analyzer,
    hipaa_compliance_sandbox,
    iso_compliance_assistant,
    pci_dss_readiness_engine,
)


class ComplianceGovernanceTests(unittest.TestCase):
    def test_compliance_governance_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ["gdpr.json", "iso.json", "pci_dss.json", "hipaa.json"]:
                (root / name).write_text(json.dumps({"controls": [{"status": "ready"}, {"status": "gap"}]}), encoding="utf-8")
            (root / "governance.json").write_text(json.dumps({"councils": [{"status": "active"}, {"status": "inactive"}], "policies": [{"status": "approved"}, {"status": "draft"}]}), encoding="utf-8")
            (root / "legal_reasoning.json").write_text(json.dumps({"briefs": [{"human_reviewed": True, "risk": "high"}, {"human_reviewed": False, "risk": "low"}]}), encoding="utf-8")
            (root / "policy_drafting.json").write_text(json.dumps({"drafts": [{"status": "approved"}, {"status": "review"}]}), encoding="utf-8")
            with patch("tools.compliance_governance_tools.COMPLIANCE_DIR", root):
                self.assertIn("Gap controls: 1", gdpr_readiness_analyzer())
                self.assertIn("Gap controls: 1", iso_compliance_assistant())
                self.assertIn("Gap controls: 1", pci_dss_readiness_engine())
                self.assertIn("Gap controls: 1", hipaa_compliance_sandbox())
                self.assertIn("Active councils: 1", enterprise_governance_framework())
                self.assertIn("High-risk briefs: 1", ai_legal_reasoning_layer())
                self.assertIn("Drafts awaiting review: 1", ai_policy_drafting_engine())

    def test_routes_cover_544_to_550(self):
        for phase in range(544, 551):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
