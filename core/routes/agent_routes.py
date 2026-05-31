from core.agents.agent_registry import list_agents, get_agent


def handle_agent_routes(user_input: str, text: str, clean_text: str):
    lowered = (text or "").lower().strip()

    if lowered in ["agents", "list agents", "show agents", "agent list"]:
        agents = list_agents()

        lines = ["Available Jarvis specialist agents:", ""]

        for agent in agents:
            lines.append(
                f"- {agent.name} ({agent.title}) — {agent.department}: {agent.objective}"
            )

        return "\n".join(lines)

    if lowered.startswith("agent "):
        key = lowered.replace("agent ", "", 1).strip()
        agent = get_agent(key)

        return (
            f"{agent.name} — {agent.title}\n"
            f"Universe: {agent.universe}\n"
            f"Department: {agent.department}\n"
            f"Objective: {agent.objective}\n"
            f"Routes: {', '.join(agent.route_names) if agent.route_names else 'None'}\n"
            f"Keywords: {', '.join(agent.keywords[:12]) if agent.keywords else 'None'}"
        )

    return None
