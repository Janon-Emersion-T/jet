import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.research_evidence_tools import *


class ResearchEvidenceTests(unittest.TestCase):
    def test_research_evidence_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "skill_library_manager.json": {"skills": [{"organized": True, "missing": True}, {"organized": False, "missing": False}]},
                "tool_learning_framework.json": {"tool_patterns": [{"learned": True, "unreliable": True}, {"learned": False, "unreliable": False}]},
                "documentation_crawler.json": {"doc_sources": [{"indexed": True, "stale": True}, {"indexed": False, "stale": False}]},
                "trusted_source_ranking.json": {"source_profiles": [{"trusted": True, "questionable": True}, {"trusted": False, "questionable": False}]},
                "local_research_cache.json": {"cache_entries": [{"fresh": True, "stale": True}, {"fresh": False, "stale": False}]},
                "evidence_first_answer_mode.json": {"answer_paths": [{"evidenced": True, "unsupported": True}, {"evidenced": False, "unsupported": False}]},
                "citation_aware_offline_notes.json": {"note_entries": [{"cited": True, "orphaned": True}, {"cited": False, "orphaned": False}]},
                "knowledge_decay_detector.json": {"knowledge_items": [{"fresh": True, "decayed": True}, {"fresh": False, "decayed": False}]},
                "stale_information_warning.json": {"information_items": [{"current": True, "warning": True}, {"current": False, "warning": False}]},
                "self_updating_knowledge_queues.json": {"update_queues": [{"flowing": True, "backlogged": True}, {"flowing": False, "backlogged": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.research_evidence_tools.RESEARCH_EVIDENCE_DIR", root):
                self.assertIn("Missing skills: 1", skill_library_manager())
                self.assertIn("Unreliable patterns: 1", tool_learning_framework())
                self.assertIn("Stale sources: 1", autonomous_documentation_crawler())
                self.assertIn("Questionable sources: 1", trusted_source_ranking_system())
                self.assertIn("Stale entries: 1", local_research_cache())
                self.assertIn("Unsupported paths: 1", evidence_first_answer_mode())
                self.assertIn("Orphaned notes: 1", citation_aware_offline_notes())
                self.assertIn("Decayed items: 1", knowledge_decay_detector())
                self.assertIn("Warning items: 1", stale_information_warning_system())
                self.assertIn("Backlogged queues: 1", self_updating_knowledge_queues())

    def test_routes_cover_1721_to_1730(self):
        for phase in range(1721, 1731):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
