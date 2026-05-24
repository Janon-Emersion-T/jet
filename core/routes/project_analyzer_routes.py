from tools.project_analyzers import (
    summarize_project_structure,
    analyze_laravel_project,
    analyze_react_project,
    analyze_python_project,
    analyze_electron_project,
)


def handle_project_analyzer_routes(user_input: str, text: str, clean_text: str):
    if text in ["summarize project", "project structure", "summarize project structure"]:
        return summarize_project_structure()

    if text in ["analyze laravel", "laravel analyzer", "analyze laravel project"]:
        return analyze_laravel_project()

    if text in ["analyze react", "react analyzer", "analyze react project"]:
        return analyze_react_project()

    if text in ["analyze python", "python analyzer", "analyze python project"]:
        return analyze_python_project()

    if text in ["analyze electron", "electron analyzer", "analyze electron project"]:
        return analyze_electron_project()

    return None
