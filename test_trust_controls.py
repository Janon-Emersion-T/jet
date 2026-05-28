import unittest

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.trust_controls_tools import (
    VerificationSample,
    adaptive_permission_escalation,
    ai_ethics_constraints,
    decision_trace_system,
    emergency_shutdown_mode,
    explain_why_engine,
    face_recognition_integration,
    risk_level_scoring_system,
    sandboxed_execution_layer,
    trusted_user_verification,
    voice_biometric_recognition,
)


class TrustControlsTests(unittest.TestCase):
    def test_explain_trace_and_ethics_render(self):
        self.assertIn("EXPLAIN-WHY ENGINE", explain_why_engine())
        self.assertIn("DECISION TRACE SYSTEM", decision_trace_system())
        self.assertIn("AI ETHICS CONSTRAINTS", ai_ethics_constraints())

    def test_shutdown_sandbox_and_risk_render(self):
        self.assertIn("EMERGENCY SHUTDOWN MODE", emergency_shutdown_mode())
        self.assertIn("SANDBOXED EXECUTION LAYER", sandboxed_execution_layer())
        self.assertIn("Label: HIGH", risk_level_scoring_system("delete production secret"))

    def test_permission_escalation_and_verification(self):
        self.assertIn("owner approval plus explicit confirmation", adaptive_permission_escalation("developer", "high"))
        sample = VerificationSample(0.9, 0.92, 0.8, 0.7)
        self.assertIn("Decision: MATCH", voice_biometric_recognition(sample))
        self.assertIn("Decision: MATCH", face_recognition_integration(sample))
        self.assertIn("Decision: TRUSTED", trusted_user_verification(sample))

    def test_routes_cover_411_to_420(self):
        for phase in range(411, 421):
            response = handle_ai_operations_routes(f"{phase} help", f"{phase} help", "")
            self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()
