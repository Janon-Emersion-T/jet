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
        "status": "not_connected",
        "description": "Cannot check live weather yet."
    },
    "location": {
        "status": "not_connected",
        "description": "Cannot detect live GPS or exact current location yet."
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
        "status": "not_connected",
        "description": "Cannot read or send email yet."
    },
    "calendar": {
        "status": "not_connected",
        "description": "Cannot manage calendar yet."
    },
    "seo_automation": {
        "status": "planned",
        "description": "SEO automation will be added later."
    },
    "web_development": {
        "status": "active",
        "description": "Can plan and execute Laravel web app builds with safe file, command, and project-scoped workflows."
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
