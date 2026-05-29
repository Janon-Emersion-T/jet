CAPABILITIES = {
    "memory": {
        "status": "active",
        "description": "Can save facts, list facts, and search previous conversations."
    },
    "system_commands": {
        "status": "active",
        "description": "Can run approved safe system commands only."
    },
    "project_discovery": {
        "status": "active",
        "description": "Can list and inspect local project folders."
    },
    "offline_voice": {
        "status": "active",
        "description": "Can listen and speak using offline voice mode."
    },
    "weather": {
        "status": "active",
        "description": "Can retrieve read-only current weather through Open-Meteo."
    },
    "location": {
        "status": "active",
        "description": "Can retrieve optional approximate IP location or use a saved location; not GPS."
    },
    "camera": {
        "status": "not_connected",
        "description": "Cannot access camera yet."
    },
    "browser_control": {
        "status": "active",
        "description": "Can open websites and perform Google searches using Playwright."
    },
    "email": {
        "status": "active",
        "description": "Can send configured SMTP mail and attention-event alerts, subject to dry-run setting."
    },
    "calendar": {
        "status": "not_connected",
        "description": "Cannot manage calendar yet."
    },
    "seo_automation": {
        "status": "planned",
        "description": "SEO automation will be added later."
    }
}

def list_capabilities() -> str:
    lines = ["JARVIS Capability Registry:"]

    for name, data in CAPABILITIES.items():
        lines.append(
            f"- {name}: {data['status']} — {data['description']}"
        )

    return "\n".join(lines)

def capability_status(name: str) -> str:
    key = name.lower().replace(" ", "_")

    if key not in CAPABILITIES:
        return f"Capability '{name}' is not registered yet."

    data = CAPABILITIES[key]
    return f"{key}: {data['status']} — {data['description']}"
