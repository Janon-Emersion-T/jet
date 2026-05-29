import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.simulation_story_tools import (
    creative_writing_engine,
    game_ai_engine,
    npc_personality_framework,
    simulation_environment_builder,
)


class SimulationStoryTests(unittest.TestCase):
    def test_writing_game_npc_and_simulation_render(self):
        with tempfile.TemporaryDirectory() as directory:
            sim_dir = Path(directory)
            (sim_dir / "writing.json").write_text(
                json.dumps({"drafts": [{"genre": "sci-fi"}, {"genre": "mystery"}]}),
                encoding="utf-8",
            )
            (sim_dir / "game_ai.json").write_text(
                json.dumps({"prototypes": [{"agent_count": 5}, {"agent_count": 3}]}),
                encoding="utf-8",
            )
            (sim_dir / "npc_profiles.json").write_text(
                json.dumps({"profiles": [{"faction": "guild"}, {"faction": "guild"}, {"faction": "rebels"}]}),
                encoding="utf-8",
            )
            (sim_dir / "scenarios.json").write_text(
                json.dumps({"scenarios": [{"environment": "city"}, {"environment": "dungeon"}]}),
                encoding="utf-8",
            )
            with patch("tools.simulation_story_tools.SIM_DIR", sim_dir):
                writing = creative_writing_engine()
                game = game_ai_engine()
                npc = npc_personality_framework()
                simulation = simulation_environment_builder()
        self.assertIn("Drafts tracked: 2", writing)
        self.assertIn("Total AI agents described: 8", game)
        self.assertIn("Factions: guild, rebels", npc)
        self.assertIn("Environment types: city, dungeon", simulation)

    def test_routes_cover_477_to_480(self):
        for phase in range(477, 481):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
