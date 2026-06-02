from tools.project_health_tools import (
    vite_build_checker,
    npm_script_runner,
    composer_script_runner,
    python_test_runner,
    php_syntax_checker,
    js_syntax_checker,
    css_tailwind_checker,
    blade_syntax_risk_checker,
    project_health_score,
    project_todo_scanner,
    code_smell_detector,
    duplicate_code_detector,
    dead_file_detector,
    missing_import_detector,
    missing_route_detector,
    missing_view_detector,
    missing_component_detector,
    db_config_checker,
    migration_status_checker,
    safe_artisan_runner,
)


def handle_project_health_routes(user_input: str, text: str, clean_text: str):
    routes = {
        "vite build checker": vite_build_checker,
        "npm script runner": npm_script_runner,
        "composer script runner": composer_script_runner,
        "python test runner": python_test_runner,
        "php syntax checker": php_syntax_checker,
        "js syntax checker": js_syntax_checker,
        "css tailwind checker": css_tailwind_checker,
        "blade syntax risk checker": blade_syntax_risk_checker,
        "project health score": project_health_score,
        "project todo scanner": project_todo_scanner,
        "code smell detector": code_smell_detector,
        "duplicate code detector": duplicate_code_detector,
        "dead file detector": dead_file_detector,
        "missing import detector": missing_import_detector,
        "missing route detector": missing_route_detector,
        "missing view detector": missing_view_detector,
        "missing component detector": missing_component_detector,
        "db config checker": db_config_checker,
        "migration status checker": migration_status_checker,
        "safe artisan runner": safe_artisan_runner,
    }

    handler = routes.get(text)
    if handler:
        return handler()

    natural_aliases = {
        "project health": project_health_score,
        "health score": project_health_score,
        "check project health": project_health_score,
        "check the project health": project_health_score,
        "project health check": project_health_score,
        "project todo": project_todo_scanner,
        "scan project todos": project_todo_scanner,
        "scan project for todos": project_todo_scanner,
        "code smells": code_smell_detector,
        "find code smells": code_smell_detector,
        "check migration status": migration_status_checker,
    }

    for phrase, mapped_handler in natural_aliases.items():
        if phrase in text:
            return mapped_handler()

    return None
