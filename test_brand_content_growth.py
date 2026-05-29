import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.brand_content_growth_tools import *


class BrandContentGrowthTests(unittest.TestCase):
    def test_brand_content_growth_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payloads = {
                "brand_voice_consistency.json": {"brand_assets": [{"consistent": True, "drifting": True}, {"consistent": False, "drifting": False}]},
                "multi_brand_content.json": {"brand_streams": [{"aligned": True, "crossed": True}, {"aligned": False, "crossed": False}]},
                "case_study_miner.json": {"project_highlights": [{"usable": True, "thin": True}, {"usable": False, "thin": False}]},
                "testimonial_extraction.json": {"testimonial_candidates": [{"quotable": True, "unclear": True}, {"quotable": False, "unclear": False}]},
                "reputation_moat_builder.json": {"reputation_assets": [{"defensible": True, "fragile": True}, {"defensible": False, "fragile": False}]},
                "thought_leadership_planner.json": {"content_themes": [{"distinctive": True, "generic": True}, {"distinctive": False, "generic": False}]},
                "founder_personal_brand.json": {"brand_moves": [{"authentic": True, "performative": True}, {"authentic": False, "performative": False}]},
                "linkedin_authority_system.json": {"linkedin_posts": [{"authoritative": True, "forgettable": True}, {"authoritative": False, "forgettable": False}]},
                "youtube_strategy_assistant.json": {"video_plans": [{"clear": True, "weak": True}, {"clear": False, "weak": False}]},
                "short_form_video_factory.json": {"video_batches": [{"publishable": True, "repetitive": True}, {"publishable": False, "repetitive": False}]},
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")
            with patch("tools.brand_content_growth_tools.BRAND_CONTENT_GROWTH_DIR", root):
                self.assertIn("Drifting assets: 1", brand_voice_consistency_engine())
                self.assertIn("Crossed streams: 1", multi_brand_content_governor())
                self.assertIn("Thin highlights: 1", automated_case_study_miner())
                self.assertIn("Unclear candidates: 1", testimonial_extraction_assistant())
                self.assertIn("Fragile assets: 1", reputation_moat_builder())
                self.assertIn("Generic themes: 1", thought_leadership_planner())
                self.assertIn("Performative moves: 1", founder_personal_brand_engine())
                self.assertIn("Forgettable posts: 1", linkedin_authority_system())
                self.assertIn("Weak plans: 1", youtube_strategy_assistant())
                self.assertIn("Repetitive batches: 1", short_form_video_factory())

    def test_routes_cover_1561_to_1570(self):
        for phase in range(1561, 1571):
            self.assertIsNotNone(handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help"))


if __name__ == "__main__":
    unittest.main()
