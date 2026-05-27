from dataclasses import dataclass
from typing import List

from core.nlp.command_execution_planner import build_execution_plan


@dataclass
class BatchRouteStep:
    step: int
    command: str
    intent: str
    route_hint: str
    status: str
    reason: str


@dataclass
class BatchRouteResult:
    original_text: str
    total_steps: int
    executable_steps: int
    blocked_steps: int
    requires_confirmation_steps: int
    steps: List[BatchRouteStep]


def prepare_route_batch(user_input: str) -> BatchRouteResult:
    plan = build_execution_plan(user_input)
    steps: List[BatchRouteStep] = []

    executable = 0
    blocked = 0
    confirmation = 0

    for item in plan.steps:
        if item.requires_confirmation:
            status = "requires_confirmation"
            confirmation += 1
        elif not item.can_execute:
            status = "blocked"
            blocked += 1
        else:
            status = "ready"
            executable += 1

        steps.append(
            BatchRouteStep(
                step=item.step,
                command=item.command,
                intent=item.intent,
                route_hint=item.route_hint,
                status=status,
                reason=item.reason,
            )
        )

    return BatchRouteResult(
        original_text=user_input,
        total_steps=plan.total_steps,
        executable_steps=executable,
        blocked_steps=blocked,
        requires_confirmation_steps=confirmation,
        steps=steps,
    )


def format_route_batch(user_input: str) -> str:
    result = prepare_route_batch(user_input)

    lines = [
        "PHASE NLP-000Q — ROUTE BATCH PROCESSOR",
        "",
        f"Original: {result.original_text}",
        f"Total steps: {result.total_steps}",
        f"Ready steps: {result.executable_steps}",
        f"Blocked steps: {result.blocked_steps}",
        f"Confirmation steps: {result.requires_confirmation_steps}",
        "",
        "Prepared Batch:",
    ]

    for step in result.steps:
        lines.extend(
            [
                "",
                f"{step.step}. {step.command}",
                f"   Intent: {step.intent}",
                f"   Route hint: {step.route_hint}",
                f"   Status: {step.status}",
                f"   Reason: {step.reason}",
            ]
        )

    return "\n".join(lines)
