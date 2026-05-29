import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.creative_media_tools import (
    ai_video_generation_pipeline,
    cinematic_storyboard_assistant,
    podcast_assistant,
    voice_cloning_sandbox,
)


class CreativeMediaTests(unittest.TestCase):
    def test_video_voice_podcast_and_storyboard_render(self):
        with tempfile.TemporaryDirectory() as directory:
            media_dir = Path(directory)
            (media_dir / "video_jobs.json").write_text(
                json.dumps({"jobs": [{"status": "queued"}, {"status": "done"}]}),
                encoding="utf-8",
            )
            (media_dir / "voice_profiles.json").write_text(
                json.dumps({"profiles": [{"name": "narrator", "consent": True}, {"name": "sample", "consent": False}]}),
                encoding="utf-8",
            )
            (media_dir / "podcasts.json").write_text(
                json.dumps({"episodes": [{"status": "planned"}, {"status": "published"}]}),
                encoding="utf-8",
            )
            (media_dir / "storyboards.json").write_text(
                json.dumps({"boards": [{"scenes": [{}, {}, {}]}]}),
                encoding="utf-8",
            )
            with patch("tools.creative_media_tools.MEDIA_DIR", media_dir), \
                    patch.dict(os.environ, {"VIDEO_GEN_BACKEND": "comfyui"}, clear=False):
                video = ai_video_generation_pipeline()
                voice = voice_cloning_sandbox()
                podcast = podcast_assistant()
                storyboard = cinematic_storyboard_assistant()
        self.assertIn("Backend: comfyui", video)
        self.assertIn("Active jobs: 1", video)
        self.assertIn("Profiles with recorded consent: 1", voice)
        self.assertIn("Unpublished episodes: 1", podcast)
        self.assertIn("Scene cards: 3", storyboard)

    def test_routes_cover_471_to_476(self):
        for phase in range(471, 477):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
