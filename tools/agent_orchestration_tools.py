from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AgentRole:
    name: str
    responsibility: str
    output: str


AGENTS: Dict[str, AgentRole] = {
    "planner": AgentRole("Planner", "Break a request into ordered steps.", "task plan"),
    "executor": AgentRole("Executor", "Carry out approved implementation steps.", "execution log"),
    "critic": AgentRole("Critic", "Review quality, risks, and missing tests.", "review findings"),
    "security": AgentRole("Security", "Check safety, secrets, and abuse cases.", "security notes"),
    "seo": AgentRole("SEO", "Optimize discoverability and search intent.", "SEO brief"),
    "marketing": AgentRole("Marketing", "Shape audience, offer, and campaign angle.", "campaign plan"),
    "coding": AgentRole("Coding", "Design and implement code changes.", "code plan"),
    "research": AgentRole("Research", "Collect evidence and summarize uncertainty.", "research brief"),
}


def _format_agent(role: AgentRole, task: str) -> str:
    return (
        f"{role.name.upper()} AGENT\n"
        f"Task: {task}\n"
        f"Responsibility: {role.responsibility}\n"
        f"Expected output: {role.output}\n"
        "Safety: advisory plan only; no external action was performed."
    )


def multi_agent_orchestration(task: str = "launch a monitored local AI service") -> str:
    sequence = ["planner", "security", "coding", "critic"]
    lines = [
        "MULTI-AGENT ORCHESTRATION - PHASE 392",
        f"Task: {task}",
        "Route:",
    ]
    lines += [f"{index}. {AGENTS[name].name}: {AGENTS[name].responsibility}" for index, name in enumerate(sequence, 1)]
    lines.append("Safety: orchestration plan only; no agent executed tools.")
    return "\n".join(lines)


def planner_agent(task: str = "complete the next roadmap phase") -> str:
    return _format_agent(AGENTS["planner"], task)


def executor_agent(task: str = "apply approved implementation steps") -> str:
    return _format_agent(AGENTS["executor"], task)


def critic_agent(task: str = "review the implementation") -> str:
    return _format_agent(AGENTS["critic"], task)


def security_agent(task: str = "review security risks") -> str:
    return _format_agent(AGENTS["security"], task)


def seo_agent(task: str = "optimize a page for search") -> str:
    return _format_agent(AGENTS["seo"], task)


def marketing_agent(task: str = "plan a campaign") -> str:
    return _format_agent(AGENTS["marketing"], task)


def coding_agent(task: str = "implement a feature") -> str:
    return _format_agent(AGENTS["coding"], task)


def research_agent(task: str = "research a decision") -> str:
    return _format_agent(AGENTS["research"], task)


def agent_roster() -> List[str]:
    return [role.name for role in AGENTS.values()]
