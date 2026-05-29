import unittest

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.agent_orchestration_tools import (
    agent_roster,
    coding_agent,
    critic_agent,
    multi_agent_orchestration,
    planner_agent,
    research_agent,
    security_agent,
)


class AgentOrchestrationTests(unittest.TestCase):
    def test_agent_roster_contains_expected_roles(self):
        roster = agent_roster()
        self.assertIn("Planner", roster)
        self.assertIn("Research", roster)

    def test_multi_agent_orchestration_includes_safety_note(self):
        report = multi_agent_orchestration("ship a feature")
        self.assertIn("Planner", report)
        self.assertIn("Safety: orchestration plan only", report)

    def test_role_agents_return_expected_headers(self):
        self.assertIn("PLANNER AGENT", planner_agent())
        self.assertIn("CRITIC AGENT", critic_agent())
        self.assertIn("SECURITY AGENT", security_agent())
        self.assertIn("CODING AGENT", coding_agent())
        self.assertIn("RESEARCH AGENT", research_agent())

    def test_routes_cover_392_to_400(self):
        for phase in range(392, 401):
            response = handle_ai_operations_routes(f"{phase} help", f"{phase} help", "")
            self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()
