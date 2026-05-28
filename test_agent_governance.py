import unittest

from core.routes.ai_operations_routes import handle_ai_operations_routes
from tools.agent_governance_tools import (
    action_logging_framework,
    agent_task_marketplace,
    ai_swarm_coordination,
    autonomous_monitoring_agent,
    finance_agent,
    human_approval_gateway,
    role_based_ai_delegation,
    scheduling_agent,
)


class AgentGovernanceTests(unittest.TestCase):
    def test_finance_and_scheduling_agents_render_headers(self):
        self.assertIn("FINANCE AGENT", finance_agent())
        self.assertIn("SCHEDULING AGENT", scheduling_agent())

    def test_monitoring_agent_aggregates_subreports(self):
        report = autonomous_monitoring_agent()
        self.assertIn("AUTONOMOUS MONITORING AGENT - PHASE 405", report)
        self.assertIn("CPU/RAM MONITORING ASSISTANT - PHASE 368", report)

    def test_swarm_and_marketplace_render(self):
        self.assertIn("Swarm route", ai_swarm_coordination())
        self.assertIn("Available specialist agents", agent_task_marketplace())

    def test_role_based_delegation_routes_security(self):
        report = role_based_ai_delegation("review security posture")
        self.assertIn("Security", report)

    def test_approval_and_logging_render(self):
        self.assertIn("HUMAN APPROVAL GATEWAY", human_approval_gateway())
        self.assertIn("ACTION LOGGING FRAMEWORK", action_logging_framework())

    def test_routes_cover_401_to_410(self):
        for phase in range(401, 411):
            response = handle_ai_operations_routes(f"{phase} help", f"{phase} help", "")
            self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()
