import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.research_synthesis_web_tools import *


class ResearchSynthesisWebTests(unittest.TestCase):
    def test_research_synthesis_web_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "web_research_task_planner.json": {"research_tasks": [{"planned": True, "fuzzy": True}, {"planned": False, "fuzzy": False}]},
                "browser_reading_comprehension.json": {"reading_passages": [{"understood": True, "uncertain": True}, {"understood": False, "uncertain": False}]},
                "source_comparison_engine.json": {"source_pairs": [{"aligned": True, "conflicting": True}, {"aligned": False, "conflicting": False}]},
                "fact_dispute_resolver.json": {"disputed_claims": [{"resolved": True, "contested": True}, {"resolved": False, "contested": False}]},
                "misinformation_risk_flagger.json": {"information_signals": [{"credible": True, "risky": True}, {"credible": False, "risky": False}]},
                "research_synthesis_dashboard.json": {"synthesis_views": [{"coherent": True, "fragmented": True}, {"coherent": False, "fragmented": False}]},
                "academic_paper_ingestion.json": {"paper_entries": [{"parsed": True, "partial": True}, {"parsed": False, "partial": False}]},
                "technical_standard_parser.json": {"standard_sections": [{"parsed": True, "unclear": True}, {"parsed": False, "unclear": False}]},
                "legal_document_comparison.json": {"document_pairs": [{"aligned": True, "divergent": True}, {"aligned": False, "divergent": False}]},
                "contract_clause_risk_scorer.json": {"clause_profiles": [{"routine": True, "risky": True}, {"routine": False, "risky": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.research_synthesis_web_tools.RESEARCH_SYNTHESIS_WEB_DIR", root):
                self.assertIn("Fuzzy tasks: 1", web_research_task_planner())
                self.assertIn("Uncertain passages: 1", browser_reading_comprehension())
                self.assertIn("Conflicting pairs: 1", source_comparison_engine())
                self.assertIn("Contested claims: 1", fact_dispute_resolver())
                self.assertIn("Risky signals: 1", misinformation_risk_flagger())
                self.assertIn("Fragmented views: 1", research_synthesis_dashboard())
                self.assertIn("Partial papers: 1", academic_paper_ingestion())
                self.assertIn("Unclear sections: 1", technical_standard_parser())
                self.assertIn("Divergent pairs: 1", legal_document_comparison())
                self.assertIn("Risky clauses: 1", contract_clause_risk_scorer())

    def test_routes_cover_1731_to_1740(self):
        for phase in range(1731, 1741):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
