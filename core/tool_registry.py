from collections import Counter

from core.agents.agent_registry import AGENTS
from core.capabilities import CAPABILITIES


CAPABILITY_COMMANDS = [
    {
        "label": "Memory Usage",
        "command": "show memory usage",
        "description": "Inspect memory health, recent facts, and stored context.",
    },
    {
        "label": "Read Logs",
        "command": "read error logs",
        "description": "Inspect the latest log output from the active project.",
    },
    {
        "label": "Laravel Log Audit",
        "command": "laravel logs",
        "description": "Analyze Laravel runtime logs for failures or regressions.",
    },
    {
        "label": "Project Health",
        "command": "project health score",
        "description": "Generate a focused health check for the workspace.",
    },
    {
        "label": "Capability Scan",
        "command": "what can you do?",
        "description": "Ask Jarvis to enumerate available capabilities.",
    },
]


def _build_capabilities():
    items = []
    for name, data in CAPABILITIES.items():
        items.append(
            {
                "name": name,
                "status": data["status"],
                "description": data["description"],
            }
        )
    return items


def _build_agents():
    agents = []
    for agent in AGENTS.values():
        agents.append(
            {
                "key": agent.key,
                "name": agent.name,
                "title": agent.title,
                "department": agent.department,
                "universe": agent.universe,
                "objective": agent.objective,
                "route_names": list(agent.route_names),
                "domains": list(agent.domains),
                "intents": list(agent.intents),
                "keywords": list(agent.keywords),
                "safety_note": agent.safety_note,
            }
        )
    return agents


def get_tool_registry():
    capabilities = _build_capabilities()
    agents = _build_agents()
    department_counts = Counter(agent["department"] for agent in agents)
    status_counts = Counter(cap["status"] for cap in capabilities)

    return {
        "summary": {
            "capabilities": len(capabilities),
            "agents": len(agents),
            "departments": len(department_counts),
            "active_capabilities": status_counts.get("active", 0),
            "planned_capabilities": status_counts.get("planned", 0),
        },
        "capabilities": capabilities,
        "agents": agents,
        "departments": [
            {"name": name, "count": count}
            for name, count in department_counts.most_common()
        ],
        "status_breakdown": [
            {"status": status, "count": count}
            for status, count in status_counts.most_common()
        ],
        "quick_actions": CAPABILITY_COMMANDS,
    }
