from dataclasses import dataclass, field
from typing import List

from tools.event_tools import emit_event


@dataclass
class IncidentAssessment:
    summary: str
    severity: str
    matched_indicators: List[str] = field(default_factory=list)
    immediate_actions: List[str] = field(default_factory=list)
    evidence_actions: List[str] = field(default_factory=list)
    communication_actions: List[str] = field(default_factory=list)


SEVERITY_RULES = {
    "CRITICAL": [
        "data breach",
        "ransomware",
        "private key",
        "api key leaked",
        "token leaked",
        "production database exposed",
        "admin account compromised",
    ],
    "HIGH": [
        "account compromised",
        "unauthorized access",
        "suspicious login",
        "malware",
        "secret exposed",
        "credential exposed",
        "production down",
    ],
    "MEDIUM": [
        "phishing",
        "unexpected email",
        "security alert",
        "failed login",
        "vulnerability",
        "strange activity",
    ],
}


def assess_incident(description: str) -> IncidentAssessment:
    summary = (description or "").strip()
    lowered = summary.lower()
    severity = "LOW"
    indicators: List[str] = []

    for level, terms in SEVERITY_RULES.items():
        found = [term for term in terms if term in lowered]
        if found:
            severity = level
            indicators = found
            break

    if severity == "CRITICAL":
        containment = [
            "Isolate affected systems or revoke the exposed credential immediately.",
            "Stop risky deployments or data-changing automation until scope is known.",
            "Preserve logs and take a timestamped record of the initial report.",
        ]
    elif severity == "HIGH":
        containment = [
            "Disable affected sessions or credentials and require re-authentication.",
            "Restrict affected access while checking the scope of activity.",
        ]
    else:
        containment = [
            "Record the report and inspect relevant logs before making disruptive changes.",
            "Avoid opening suspicious links or running untrusted commands.",
        ]

    return IncidentAssessment(
        summary=summary or "No incident description supplied.",
        severity=severity,
        matched_indicators=indicators,
        immediate_actions=containment,
        evidence_actions=[
            "Capture times, account identifiers, affected systems, and observable symptoms.",
            "Preserve original messages, audit logs, screenshots, and relevant command history.",
            "Do not delete evidence or rotate logs before collecting a copy.",
        ],
        communication_actions=[
            "Notify the responsible owner if access, credentials, production, or customer data may be affected.",
            "Obtain approval before destructive remediation or external disclosure.",
        ],
    )


def incident_response_assistant(description: str = "") -> str:
    assessment = assess_incident(description)
    lines = [
        "INCIDENT RESPONSE ASSISTANT - PHASE 353",
        "",
        f"Incident: {assessment.summary}",
        f"Severity: {assessment.severity}",
        f"Indicators: {', '.join(assessment.matched_indicators) or 'No high-confidence indicator identified'}",
        "",
        "Immediate containment:",
    ]
    lines.extend(f"- {action}" for action in assessment.immediate_actions)
    lines.append("")
    lines.append("Preserve evidence:")
    lines.extend(f"- {action}" for action in assessment.evidence_actions)
    lines.append("")
    lines.append("Communication and approval:")
    lines.extend(f"- {action}" for action in assessment.communication_actions)
    lines.extend([
        "",
        "Safety:",
        "- Planning and triage only. No system, account, or file was changed.",
        "- Use `report security incident <description>` to deliberately create an attention alert.",
    ])
    return "\n".join(lines)


def report_security_incident(description: str) -> str:
    assessment = assess_incident(description)
    delivery = emit_event(
        "SECURITY_INCIDENT_REPORTED",
        f"{assessment.severity} security incident requires attention",
        assessment.summary,
        requires_attention=True,
    )
    return (
        incident_response_assistant(description)
        + "\n\nAttention notification:\n- "
        + delivery
    )
