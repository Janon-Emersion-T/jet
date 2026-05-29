import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.distributed_ai_tools import (
    distributed_memory_system,
    federated_local_ai_network,
    sovereign_ai_workstation,
)


class DistributedAITests(unittest.TestCase):
    def test_federation_memory_and_workstation_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "federation.json").write_text(
                json.dumps({"peers": [{"trusted": True}, {"trusted": False}]}),
                encoding="utf-8",
            )
            (root / "memory_shards.json").write_text(
                json.dumps({"stores": [{"replicas": 2}, {"replicas": 3}]}),
                encoding="utf-8",
            )
            (root / "workstation.json").write_text(
                json.dumps({"gpus": 2, "ram_gb": 128, "secure_boot": True}),
                encoding="utf-8",
            )
            with patch("tools.distributed_ai_tools.DISTRIBUTED_DIR", root):
                federation = federated_local_ai_network()
                memory = distributed_memory_system()
                workstation = sovereign_ai_workstation()
        self.assertIn("Peers tracked: 2", federation)
        self.assertIn("Trusted peers: 1", federation)
        self.assertIn("Replica count: 5", memory)
        self.assertIn("Secure boot enabled: YES", workstation)

    def test_routes_cover_486_to_492(self):
        for phase in range(486, 493):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
