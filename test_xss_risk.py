import tempfile
import unittest
from pathlib import Path

from core.routes.security_routes import handle_security_routes
from tools.xss_risk_tools import detect_xss_risks, xss_risk_detector


class XSSRiskTests(unittest.TestCase):
    def test_detects_framework_specific_rendering_sinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Panel.jsx").write_text(
                "<div dangerouslySetInnerHTML={{__html: userHtml}} />\n",
                encoding="utf-8",
            )
            (root / "show.blade.php").write_text("{!! $comment !!}\n", encoding="utf-8")
            _, findings, error = detect_xss_risks(root)
        self.assertIsNone(error)
        self.assertTrue(any(item.framework == "React" for item in findings))
        self.assertTrue(any(item.framework == "Laravel Blade" for item in findings))

    def test_escaped_template_has_no_configured_sink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "safe.blade.php").write_text("{{ $comment }}\n", encoding="utf-8")
            report = xss_risk_detector(root)
        self.assertIn("Potential sinks: 0", report)

    def test_route_exposes_phase_356_help(self):
        report = handle_security_routes("356 help", "356 help", "")
        self.assertIn("XSS RISK DETECTOR COMMANDS - PHASE 356", report)


if __name__ == "__main__":
    unittest.main()
