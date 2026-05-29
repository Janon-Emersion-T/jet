import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes


def assert_phase_module(test_case, module):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for config in module.PHASE_CONFIGS:
            payload = {
                config.get("collection_key", "records"): [
                    {config.get("healthy_flag", "healthy"): True, config.get("attention_flag", "attention"): True},
                    {config.get("healthy_flag", "healthy"): False, config.get("attention_flag", "attention"): False},
                ]
            }
            (root / config["filename"]).write_text(json.dumps(payload), encoding="utf-8")
        with patch.object(module, "MODULE_DIR", root):
            for config in module.PHASE_CONFIGS:
                handler = getattr(module, config["name"])
                output = handler()
                test_case.assertIn(f"PHASE {config['phase']}", output)
                test_case.assertIn("Healthy signals: 1", output)
                test_case.assertIn("Attention signals: 1", output)
                test_case.assertIsNotNone(handle_ai_operations_routes(f"{config['phase']} help", f"{config['phase']} help", f"{config['phase']} help"))
