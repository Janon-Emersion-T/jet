import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.memory_knowledge_runtime_tools import *


class MemoryKnowledgeRuntimeTests(unittest.TestCase):
    def test_memory_knowledge_runtime_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "hallucination_suppression.json": {"answer_checks": [{"grounded": True, "speculative": True}, {"grounded": False, "speculative": False}]},
                "tool_call_validation_engine.json": {"tool_calls": [{"validated": True, "unsafe": True}, {"validated": False, "unsafe": False}]},
                "memory_contradiction_resolver.json": {"memory_pairs": [{"resolved": True, "conflicting": True}, {"resolved": False, "conflicting": False}]},
                "long_term_knowledge_curator.json": {"knowledge_entries": [{"curated": True, "stale": True}, {"curated": False, "stale": False}]},
                "personal_ontology_builder.json": {"ontology_nodes": [{"linked": True, "orphaned": True}, {"linked": False, "orphaned": False}]},
                "work_context_summarizer.json": {"context_summaries": [{"useful": True, "lossy": True}, {"useful": False, "lossy": False}]},
                "active_project_memory_injection.json": {"memory_packets": [{"relevant": True, "irrelevant": True}, {"relevant": False, "irrelevant": False}]},
                "episodic_memory_timeline.json": {"episodes": [{"ordered": True, "ambiguous": True}, {"ordered": False, "ambiguous": False}]},
                "semantic_memory_graph.json": {"graph_edges": [{"grounded": True, "speculative": True}, {"grounded": False, "speculative": False}]},
                "procedural_memory_engine.json": {"procedures": [{"reusable": True, "fragile": True}, {"reusable": False, "fragile": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.memory_knowledge_runtime_tools.MEMORY_KNOWLEDGE_RUNTIME_DIR", root):
                self.assertIn("Speculative checks: 1", hallucination_suppression_layer())
                self.assertIn("Unsafe calls: 1", tool_call_validation_engine())
                self.assertIn("Conflicting pairs: 1", memory_contradiction_resolver())
                self.assertIn("Stale entries: 1", long_term_knowledge_curator())
                self.assertIn("Orphaned nodes: 1", personal_ontology_builder())
                self.assertIn("Lossy summaries: 1", work_context_summarizer())
                self.assertIn("Irrelevant packets: 1", active_project_memory_injection())
                self.assertIn("Ambiguous episodes: 1", episodic_memory_timeline())
                self.assertIn("Speculative edges: 1", semantic_memory_graph())
                self.assertIn("Fragile procedures: 1", procedural_memory_engine())

    def test_routes_cover_1711_to_1720(self):
        for phase in range(1711, 1721):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
