import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.nlp.domain_understanding import understand_domain
from core.nlp.file_awareness import understand_file_command
from core.nlp.safety_planner import plan_safe_command
from core.nlp.target_resolvers import resolve_targets
from core.nlp.task_planner import build_task_plan
from core.nlp.unified_orchestrator import format_unified_report, orchestrate_command
from core.nlp.voice_understanding import parse_voice_intent


class ModularNLPTests(unittest.TestCase):
    def test_file_awareness_resolves_a_project_file(self):
        result = understand_file_command("read file main.py", project_root=".")
        self.assertEqual(result.action, "read")
        self.assertTrue(result.targets[0].exists)
        self.assertTrue(result.targets[0].within_project)

    def test_dangerous_commands_are_explained_and_denied_for_operator(self):
        decision = plan_safe_command("rm -rf storage")
        self.assertEqual(decision.safety_level, "dangerous")
        self.assertTrue(decision.requires_confirmation)
        self.assertFalse(decision.allowed)
        self.assertTrue(decision.reasons)
        self.assertTrue(decision.alternatives)

    def test_target_resolvers_are_independent_and_composable(self):
        targets = resolve_targets("review main.py then visit https://example.com")
        self.assertTrue(targets.file.endswith("main.py"))
        self.assertEqual(targets.browser, "https://example.com")

    def test_task_planner_marks_writes_for_approval(self):
        plan = build_task_plan("read main.py then update main.py")
        self.assertEqual(len(plan.steps), 2)
        self.assertTrue(plan.steps[1].approval_required)
        self.assertTrue(plan.requires_human_approval)

    def test_voice_and_domain_understanding(self):
        voice = parse_voice_intent("hey jabbies please confirm")
        self.assertTrue(voice.wake_word_detected)
        self.assertTrue(voice.confirmation)
        domain = understand_domain("review python api test code")
        self.assertEqual(domain.domain, "developer")

    def test_unified_orchestrator_composes_features(self):
        with tempfile.TemporaryDirectory() as directory:
            memory_path = Path(directory) / "intent_memory.json"
            audit_path = Path(directory) / "audit_trail.jsonl"
            cache_path = Path(directory) / "semantic_cache.json"
            with patch("core.nlp.intent_memory.MEMORY_FILE", memory_path), \
                    patch("core.nlp.safety_planner.AUDIT_FILE", audit_path), \
                    patch("core.nlp.runtime_services.CACHE_FILE", cache_path):
                result = orchestrate_command("read file main.py", audit=False)
                report = format_unified_report("read file main.py")
        self.assertIsNotNone(result.file_awareness.primary_target)
        self.assertEqual(result.intent, "project_analysis")
        self.assertIn("Semantic cache hit: YES", report)
        self.assertIn("FINAL UNIFIED NLP ORCHESTRATOR", report)

    def test_unified_orchestrator_gates_original_destructive_text(self):
        with tempfile.TemporaryDirectory() as directory:
            memory_path = Path(directory) / "intent_memory.json"
            cache_path = Path(directory) / "semantic_cache.json"
            with patch("core.nlp.intent_memory.MEMORY_FILE", memory_path), \
                    patch("core.nlp.runtime_services.CACHE_FILE", cache_path):
                result = orchestrate_command("rm -rf storage", audit=False)
        self.assertEqual(result.safety.safety_level, "dangerous")
        self.assertFalse(result.safety.allowed)


if __name__ == "__main__":
    unittest.main()
