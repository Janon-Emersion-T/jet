import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.sql_injection_risk_tools import detect_sql_injection_risks, sql_injection_risk_detector


class SQLInjectionRiskTests(unittest.TestCase):
    def test_detects_python_and_laravel_dynamic_sql(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "repository.py").write_text(
                'cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")\n',
                encoding="utf-8",
            )
            (root / "UserController.php").write_text(
                'DB::select("SELECT * FROM users WHERE email = \'$email\'");\n',
                encoding="utf-8",
            )
            _, findings, error = detect_sql_injection_risks(root)
        self.assertIsNone(error)
        self.assertTrue(any(item.language == "Python DB-API" for item in findings))
        self.assertTrue(any(item.language == "Laravel/PHP" for item in findings))

    def test_parameterized_query_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "repository.py").write_text(
                'cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))\n',
                encoding="utf-8",
            )
            report = sql_injection_risk_detector(root)
        self.assertIn("Possible sinks: 0", report)

    def test_route_exposes_phase_358_help(self):
        report = handle_security_routes("358 help", "358 help", "")
        self.assertIn("SQL INJECTION RISK DETECTOR COMMANDS - PHASE 358", report)


if __name__ == "__main__":
    unittest.main()
