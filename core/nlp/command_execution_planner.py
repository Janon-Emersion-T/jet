from dataclasses import dataclass, field
from typing import Dict, List

from core.nlp.multi_intent_parser import parse_multi_intent_command
from core.nlp.phase000_engine import analyze_command


@dataclass
class PlannedCommand:
    step: int
    command: str
    intent: str
    route_hint: str
    confidence: float
    safety_level: str
    can_execute: bool
    requires_confirmation: bool
    reason: str
    entities: Dict[str, str] = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    original_text: str
    total_steps: int
    is_batch: bool
    safe_to_run: bool
    steps: List[PlannedCommand]


BLOCKED_SAFETY_LEVELS = ["dangerous"]
CONFIRMATION_SAFETY_LEVELS = ["needs_confirmation"]


def build_execution_plan(user_input: str) -> ExecutionPlan:
    parsed = parse_multi_intent_command(user_input)
    steps: List[PlannedCommand] = []

    for item in parsed.commands:
        nlp = analyze_command(item.clean_text)

        requires_confirmation = nlp.safety_level in CONFIRMATION_SAFETY_LEVELS
        blocked = nlp.safety_level in BLOCKED_SAFETY_LEVELS

        can_execute = not blocked and nlp.confidence >= 0.35

        if blocked:
            reason = "Blocked because the command is classified as dangerous."
        elif requires_confirmation:
            reason = "Allowed only after explicit confirmation."
        elif nlp.confidence < 0.35:
            reason = "Low confidence. Needs clarification before execution."
        else:
            reason = "Command is safe for planned routing."

        steps.append(
            PlannedCommand(
                step=item.index,
                command=nlp.clean_text,
                intent=nlp.intent,
                route_hint=nlp.route_hint or "none",
                confidence=nlp.confidence,
                safety_level=nlp.safety_level,
                can_execute=can_execute,
                requires_confirmation=requires_confirmation,
                reason=reason,
                entities=nlp.entities,
            )
        )

    safe_to_run = all(step.can_execute and not step.requires_confirmation for step in steps)

    return ExecutionPlan(
        original_text=user_input,
        total_steps=len(steps),
        is_batch=parsed.is_multi_intent,
        safe_to_run=safe_to_run,
        steps=steps,
    )


def format_execution_plan(user_input: str) -> str:
    plan = build_execution_plan(user_input)

    lines = [
        "PHASE NLP-000P — COMMAND EXECUTION PLANNER",
        "",
        f"Original: {plan.original_text}",
        f"Batch command: {'YES' if plan.is_batch else 'NO'}",
        f"Total steps: {plan.total_steps}",
        f"Safe to run automatically: {'YES' if plan.safe_to_run else 'NO'}",
        "",
        "Execution Plan:",
    ]

    for step in plan.steps:
        lines.extend(
            [
                "",
                f"{step.step}. {step.command}",
                f"   Intent: {step.intent}",
                f"   Route hint: {step.route_hint}",
                f"   Confidence: {step.confidence}",
                f"   Safety: {step.safety_level}",
                f"   Can execute: {'YES' if step.can_execute else 'NO'}",
                f"   Requires confirmation: {'YES' if step.requires_confirmation else 'NO'}",
                f"   Reason: {step.reason}",
            ]
        )

    return "\n".join(lines)
