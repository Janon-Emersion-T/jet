import unittest
from unittest.mock import patch

from core.routes.security_routes import handle_security_routes
from tools.security_response_tools import (
    assess_incident,
    incident_response_assistant,
    report_security_incident,
)


class IncidentResponseTests(unittest.TestCase):
    def test_critical_indicator_produces_immediate_containment_plan(self):
        assessment = assess_incident("Our production API key leaked in a public commit")
        self.assertEqual(assessment.severity, "CRITICAL")
        self.assertIn("api key leaked", assessment.matched_indicators)
        self.assertIn("revoke", assessment.immediate_actions[0].lower())

    def test_analysis_is_read_only_and_does_not_emit_event(self):
        with patch("tools.security_response_tools.emit_event") as event:
            report = incident_response_assistant("Suspicious login on the admin dashboard")
        event.assert_not_called()
        self.assertIn("Severity: HIGH", report)
        self.assertIn("Planning and triage only", report)

    def test_explicit_report_emits_attention_event(self):
        with patch("tools.security_response_tools.emit_event", return_value="System email sent.") as event:
            report = report_security_incident("A token leaked from production")
        event.assert_called_once()
        self.assertTrue(event.call_args.kwargs["requires_attention"])
        self.assertIn("Attention notification", report)

    def test_route_handles_natural_grace_followup_body(self):
        report = handle_security_routes(
            "help me respond to unauthorized access in production",
            "help me respond to unauthorized access in production",
            "",
        )
        self.assertIn("INCIDENT RESPONSE ASSISTANT - PHASE 353", report)
        self.assertIn("Severity: HIGH", report)


if __name__ == "__main__":
    unittest.main()
