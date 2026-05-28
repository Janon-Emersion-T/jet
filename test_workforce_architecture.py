import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.workforce_architecture_tools import (
    ai_company_workforce_ecosystem,
    ai_executive_assistant_framework,
    jarvis_prime_architecture_foundation,
)


class WorkforceArchitectureTests(unittest.TestCase):
    def test_executive_workforce_and_prime_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "executive_framework.json").write_text(
                json.dumps({"briefs": [{"title": "weekly"}], "cadences": [{"name": "monday review"}]}),
                encoding="utf-8",
            )
            (root / "workforce.json").write_text(
                json.dumps({"roles": [{"name": "ops"}], "automations": [{"name": "triage"}, {"name": "reporting"}]}),
                encoding="utf-8",
            )
            (root / "jarvis_prime.json").write_text(
                json.dumps({"layers": [{"name": "nlp"}, {"name": "runtime"}], "principles": [{"name": "governance"}]}),
                encoding="utf-8",
            )
            with patch("tools.workforce_architecture_tools.WORKFORCE_DIR", root):
                executive = ai_executive_assistant_framework()
                workforce = ai_company_workforce_ecosystem()
                prime = jarvis_prime_architecture_foundation()
        self.assertIn("Executive briefs: 1", executive)
        self.assertIn("Automation programs: 2", workforce)
        self.assertIn("Architecture layers: 2", prime)
        self.assertIn("Guiding principles: 1", prime)

    def test_routes_cover_498_to_500(self):
        for phase in range(498, 501):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
