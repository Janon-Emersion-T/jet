import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.runtime_detection_tools import (
    ai_intrusion_detection,
    ai_malware_behavior_analyzer,
    behavioral_firewall_system,
    real_time_anomaly_detection,
    runtime_threat_analysis,
)


class RuntimeDetectionTests(unittest.TestCase):
    def test_runtime_detection_render(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "runtime_threats.json").write_text(
                json.dumps(
                    {
                        "findings": [
                            {"severity": "critical", "status": "open"},
                            {"severity": "medium", "status": "mitigated"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (root / "intrusion_detection.json").write_text(
                json.dumps(
                    {
                        "detections": [
                            {"confidence": "high", "lateral_movement": True},
                            {"confidence": "low", "lateral_movement": False},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (root / "anomaly_detection.json").write_text(
                json.dumps(
                    {
                        "anomalies": [
                            {"status": "active", "severity": "high"},
                            {"status": "closed", "severity": "low"},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (root / "malware_behavior.json").write_text(
                json.dumps(
                    {
                        "samples": [
                            {"classification": "malicious", "stealthy": True},
                            {"classification": "benign", "stealthy": False},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (root / "behavioral_firewall.json").write_text(
                json.dumps(
                    {
                        "policies": [{"mode": "learning"}, {"mode": "enforcing"}],
                        "events": [{"action": "blocked"}, {"action": "allowed"}],
                    }
                ),
                encoding="utf-8",
            )
            with patch("tools.runtime_detection_tools.RUNTIME_SECURITY_DIR", root):
                threats = runtime_threat_analysis()
                intrusions = ai_intrusion_detection()
                anomalies = real_time_anomaly_detection()
                malware = ai_malware_behavior_analyzer()
                firewall = behavioral_firewall_system()
        self.assertIn("Threat findings: 2", threats)
        self.assertIn("Critical findings: 1", threats)
        self.assertIn("Detections tracked: 2", intrusions)
        self.assertIn("Lateral-movement detections: 1", intrusions)
        self.assertIn("Anomalies tracked: 2", anomalies)
        self.assertIn("High-severity anomalies: 1", anomalies)
        self.assertIn("Behavior samples: 2", malware)
        self.assertIn("Stealthy samples: 1", malware)
        self.assertIn("Firewall policies: 2", firewall)
        self.assertIn("Blocked behavior events: 1", firewall)

    def test_routes_cover_531_to_535(self):
        for phase in range(531, 536):
            result = handle_ai_operations_routes(f"{phase} help", f"{phase} help", f"{phase} help")
            self.assertIsNotNone(result, f"missing route for {phase}")


if __name__ == "__main__":
    unittest.main()
