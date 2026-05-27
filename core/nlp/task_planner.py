from dataclasses import dataclass, field
import re
from typing import List, Optional

from core.nlp.safety_planner import SafetyDecision, classify_action, gate_route


@dataclass
class TaskStep:
    number: int
    instruction: str
    action_type: str
    agent: str
    tool: str
    depends_on: List[int] = field(default_factory=list)
    approval_required: bool = False
    executable: bool = True
    reason: str = ""


@dataclass
class TaskPlan:
    original_text: str
    steps: List[TaskStep]
    requires_human_approval: bool


def decompose_task(text: str) -> List[str]:
    parts = re.split(r"\s+(?:and then|then|after that|next)\s+|[;\n]+", text or "", flags=re.I)
    return [part.strip() for part in parts if part.strip()] or ([text.strip()] if text.strip() else [])


def select_agent(instruction: str, route_hint: Optional[str] = None) -> str:
    text = instruction.lower()
    route = route_hint or ""
    if any(word in text for word in ["unsafe", "security", "vulnerability", "rm -rf", "permission"]):
        return "Grace (Security Expert)"
    if route in {"github", "devops"} or any(word in text for word in ["git", "deploy", "server"]):
        return "Linus (DevOps Engineer)"
    if route == "database" or any(word in text for word in ["sql", "database", "migration"]):
        return "Edgar (Database Expert)"
    if route == "browser" or "http" in text:
        return "Alfred (Main Assistant)"
    if route == "file" or any(word in text for word in ["file", "code", "test"]):
        return "Ada (Programmer)"
    return "Alfred (Main Assistant)"


def select_tool(instruction: str, action_type: str, route_hint: Optional[str] = None) -> str:
    route = route_hint or ""
    if route == "file":
        return "safe_file_writer" if action_type == "write" else "project_file_reader"
    if route == "github":
        return "git_inspector"
    if route == "browser":
        return "browser_automation"
    if route == "database":
        return "database_analyzer"
    return "command_router"


def build_task_plan(text: str, route_hint: Optional[str] = None,
                    user_role: str = "operator") -> TaskPlan:
    steps = []
    previous_write = None
    for number, instruction in enumerate(decompose_task(text), start=1):
        decision: SafetyDecision = gate_route(instruction, route_hint, user_role)
        action = classify_action(instruction)
        dependencies = [previous_write] if previous_write and action == "write" else []
        steps.append(TaskStep(
            number=number,
            instruction=instruction,
            action_type=action,
            agent=select_agent(instruction, route_hint),
            tool=select_tool(instruction, action, route_hint),
            depends_on=dependencies,
            approval_required=decision.requires_confirmation,
            executable=decision.allowed,
            reason="; ".join(decision.reasons),
        ))
        if action == "write":
            previous_write = number
    return TaskPlan(
        original_text=text,
        steps=steps,
        requires_human_approval=any(step.approval_required for step in steps),
    )


def approval_workflow(plan: TaskPlan) -> List[str]:
    return [
        f"Approve step {step.number}: {step.instruction}"
        for step in plan.steps if step.approval_required
    ]
