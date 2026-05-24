from tools.framework_inspectors import (
    analyze_python_traceback,
    analyze_node_error,
    auto_fix_proposal_from_error,
    inspect_routes,
    inspect_laravel_controllers,
    inspect_laravel_models,
    inspect_laravel_migrations,
    inspect_laravel_blade,
    inspect_livewire,
    inspect_filament,
)


def handle_framework_routes(user_input: str, text: str, clean_text: str):
    if text.startswith("analyze python traceback :::"):
        error_text = user_input.split(":::", 1)[1].strip()
        return analyze_python_traceback(error_text)

    if text.startswith("analyze node error :::"):
        error_text = user_input.split(":::", 1)[1].strip()
        return analyze_node_error(error_text)

    if text.startswith("propose fix from error :::"):
        error_text = user_input.split(":::", 1)[1].strip()
        return auto_fix_proposal_from_error(error_text)

    if text in ["route inspector", "inspect routes", "laravel route inspector"]:
        return inspect_routes()

    if text in ["controller inspector", "laravel controller inspector", "inspect controllers"]:
        return inspect_laravel_controllers()

    if text in ["model inspector", "laravel model inspector", "inspect models"]:
        return inspect_laravel_models()

    if text in ["migration inspector", "laravel migration inspector", "inspect migrations"]:
        return inspect_laravel_migrations()

    if text in ["blade inspector", "laravel blade inspector", "inspect blade"]:
        return inspect_laravel_blade()

    if text in ["livewire inspector", "inspect livewire"]:
        return inspect_livewire()

    if text in ["filament inspector", "inspect filament"]:
        return inspect_filament()

    return None
