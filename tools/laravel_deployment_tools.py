from __future__ import annotations

import json
from pathlib import Path


LARAVEL_DEPLOYMENT_DIR = Path("storage/laravel_deployment")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(LARAVEL_DEPLOYMENT_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def laravel_architecture_autopilot() -> str:
    return _render("LARAVEL ARCHITECTURE AUTOPILOT - PHASE 1601", "laravel-architecture overview", "laravel_architecture_autopilot.json", "architecture_reviews", "coherent", "sprawling", "Architecture reviews tracked", "Coherent reviews", "Sprawling reviews", "Guardrail: architecture guidance should preserve framework conventions, explicit tradeoffs, and avoid sweeping refactors without evidence.")


def filament_resource_architect() -> str:
    return _render("FILAMENT RESOURCE ARCHITECT - PHASE 1602", "filament-resource overview", "filament_resource_architect.json", "resource_patterns", "clean", "messy", "Resource patterns tracked", "Clean patterns", "Messy patterns", "Guardrail: Filament guidance should preserve admin usability, policy boundaries, and alignment with project conventions.")


def livewire_component_strategist() -> str:
    return _render("LIVEWIRE COMPONENT STRATEGIST - PHASE 1603", "livewire-component overview", "livewire_component_strategist.json", "component_patterns", "maintainable", "fragile", "Component patterns tracked", "Maintainable patterns", "Fragile patterns", "Guardrail: Livewire strategy should preserve state clarity, testability, and avoid brittle magic where explicit code is safer.")


def blade_ui_refactor_engine() -> str:
    return _render("BLADE UI REFACTOR ENGINE - PHASE 1604", "blade-ui-refactor overview", "blade_ui_refactor_engine.json", "ui_templates", "clean", "duplicated", "UI templates tracked", "Clean templates", "Duplicated templates", "Guardrail: Blade refactors should preserve rendering behavior, accessibility, and established component conventions.")


def tailwind_design_system_generator() -> str:
    return _render("TAILWIND DESIGN-SYSTEM GENERATOR - PHASE 1605", "tailwind-design-system overview", "tailwind_design_system.json", "design_tokens", "cohesive", "drifting", "Design tokens tracked", "Cohesive tokens", "Drifting tokens", "Guardrail: design-system generation should preserve usability, semantic naming, and compatibility with the existing UI surface.")


def vite_build_intelligence() -> str:
    return _render("VITE BUILD INTELLIGENCE - PHASE 1606", "vite-build overview", "vite_build_intelligence.json", "build_profiles", "healthy", "fragile", "Build profiles tracked", "Healthy profiles", "Fragile profiles", "Guardrail: build analysis should preserve environment specificity, avoid speculative fixes, and keep production/runtime differences visible.")


def php_fpm_diagnostic_assistant() -> str:
    return _render("PHP-FPM DIAGNOSTIC ASSISTANT - PHASE 1607", "php-fpm-diagnostics overview", "php_fpm_diagnostics.json", "fpm_checks", "healthy", "degraded", "FPM checks tracked", "Healthy checks", "Degraded checks", "Guardrail: diagnostics should preserve system safety, highlight evidence, and avoid presenting heuristics as certainty.")


def nginx_deployment_brain() -> str:
    return _render("NGINX DEPLOYMENT BRAIN - PHASE 1608", "nginx-deployment overview", "nginx_deployment_brain.json", "deployment_paths", "ready", "risky", "Deployment paths tracked", "Ready paths", "Risky paths", "Guardrail: deployment guidance should preserve rollback planning, config provenance, and environment-specific caveats.")


def shared_hosting_compatibility_autopilot() -> str:
    return _render("SHARED-HOSTING COMPATIBILITY AUTOPILOT - PHASE 1609", "shared-hosting overview", "shared_hosting_compatibility.json", "compatibility_checks", "compatible", "blocked", "Compatibility checks tracked", "Compatible checks", "Blocked checks", "Guardrail: shared-hosting analysis should preserve provider-specific limits and avoid assuming root-level capabilities.")


def vps_migration_planner() -> str:
    return _render("VPS MIGRATION PLANNER - PHASE 1610", "vps-migration overview", "vps_migration_planner.json", "migration_steps", "planned", "risky", "Migration steps tracked", "Planned steps", "Risky steps", "Guardrail: migration planning should preserve cutover safety, rollback paths, and explicit downtime assumptions.")
