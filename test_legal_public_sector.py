import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.legal_public_sector_tools import *


class LegalPublicSectorTests(unittest.TestCase):
    def test_legal_public_sector_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "law_research.json": {"matters": [{"sourced": True, "open_questions": True}, {"sourced": False, "open_questions": False}]},
                "case_law.json": {"cases": [{"precedent": True, "conflicting": True}, {"precedent": False, "conflicting": False}]},
                "legal_risk.json": {"items": [{"risk": "high", "reviewed": True}, {"risk": "low", "reviewed": False}]},
                "court_documents.json": {"documents": [{"parsed": True, "priority": "urgent"}, {"parsed": False, "priority": "normal"}]},
                "compliance_drafting.json": {"drafts": [{"status": "approved", "exceptions": True}, {"status": "draft", "exceptions": False}]},
                "government_ops.json": {"programs": [{"status": "active"}, {"status": "delayed"}]},
                "public_service.json": {"services": [{"digital": True, "status": "backlog"}, {"digital": False, "status": "live"}]},
                "smart_city.json": {"systems": [{"integrated": True, "alert": True}, {"integrated": False, "alert": False}]},
                "urban_traffic.json": {"corridors": [{"optimized": True, "status": "congested"}, {"optimized": False, "status": "clear"}]},
                "emergency_response.json": {"incidents": [{"coordinated": True, "severity": "severe"}, {"coordinated": False, "severity": "low"}]},
                "disaster_simulation.json": {"simulations": [{"status": "complete", "impact": "high"}, {"status": "draft", "impact": "low"}]},
                "rescue_planning.json": {"plans": [{"status": "approved", "time_critical": True}, {"status": "draft", "time_critical": False}]},
                "defense_simulation.json": {"exercises": [{"simulated": True, "bounded": True}, {"simulated": False, "bounded": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.legal_public_sector_tools.LEGAL_PUBLIC_DIR", root):
                self.assertIn("Sourced matters: 1", ai_law_research_engine())
                self.assertIn("Conflicting cases: 1", case_law_intelligence_assistant())
                self.assertIn("High-risk items: 1", legal_risk_scoring_system())
                self.assertIn("Urgent documents: 1", ai_court_document_analyzer())
                self.assertIn("Drafts with exceptions: 1", autonomous_compliance_drafting())
                self.assertIn("Delayed programs: 1", government_operations_intelligence())
                self.assertIn("Backlogged services: 1", public_service_ai_framework())
                self.assertIn("Alerting systems: 1", smart_city_orchestration())
                self.assertIn("Congested corridors: 1", urban_traffic_optimization())
                self.assertIn("Severe incidents: 1", emergency_response_coordination())
                self.assertIn("High-impact simulations: 1", disaster_simulation_engine())
                self.assertIn("Time-critical plans: 1", autonomous_rescue_planning())
                self.assertIn("Bounded exercises: 1", ai_defense_simulation_layer())

    def test_routes_cover_638_to_650(self):
        for phase in range(638, 651):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
