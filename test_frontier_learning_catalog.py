import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import programming_knowledge_tools as pkt


class FrontierLearningCatalogTests(unittest.TestCase):
    def test_frontier_topics_are_loaded_into_catalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            category = root / "programming.json"
            senior = root / "senior.json"
            autonomous = root / "autonomous.json"
            frontier = root / "frontier.json"

            category.write_text(json.dumps({"topics": [{"topic": "Existing Topic"}]}), encoding="utf-8")
            senior.write_text(json.dumps({"topics": []}), encoding="utf-8")
            autonomous.write_text(json.dumps({"topics": []}), encoding="utf-8")
            frontier.write_text(
                json.dumps({"topics": [{"topic": "Frontier Topic", "source_groups": ["ai-ml"]}]}),
                encoding="utf-8",
            )

            with patch.object(pkt, "CATEGORY_FILE", category), patch.object(pkt, "SENIOR_LANGUAGE_FILE", senior), patch.object(
                pkt, "AUTONOMOUS_TOPICS_FILE", autonomous
            ), patch.object(pkt, "FRONTIER_TOPICS_FILE", frontier):
                catalog = pkt._load_catalog()

        topics = [topic.get("topic") for topic in catalog.get("topics", [])]
        self.assertIn("Existing Topic", topics)
        self.assertIn("Frontier Topic", topics)


if __name__ == "__main__":
    unittest.main()
