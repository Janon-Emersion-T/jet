import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.research_intelligence_tools import (
    ai_patent_research_assistant,
    research_paper_intelligence_engine,
    scientific_literature_summarizer,
)


class ResearchIntelligenceTests(unittest.TestCase):
    def test_research_intelligence_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "paper_intelligence.json").write_text(json.dumps({"papers": [{"indexed": True, "priority": True}, {"indexed": False, "priority": False}]}), encoding="utf-8")
            (root / "literature_summaries.json").write_text(json.dumps({"summaries": [{"reviewed": True, "uncertain": True}, {"reviewed": False, "uncertain": False}]}), encoding="utf-8")
            (root / "patent_research.json").write_text(json.dumps({"patents": [{"relevant": True, "blocking": True}, {"relevant": False, "blocking": False}]}), encoding="utf-8")
            with patch("tools.research_intelligence_tools.RESEARCH_INTEL_DIR", root):
                self.assertIn("Priority papers: 1", research_paper_intelligence_engine())
                self.assertIn("Uncertain summaries: 1", scientific_literature_summarizer())
                self.assertIn("Potential blocking patents: 1", ai_patent_research_assistant())

    def test_routes_cover_598_to_600(self):
        for phase in range(598, 601):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
