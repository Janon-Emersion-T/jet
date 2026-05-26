from tools.architecture_quality_tools import (
    refactor_planner,
    architecture_consistency_checker,
    naming_convention_analyzer,
    solid_principle_analyzer,
    clean_code_scorer,
    design_pattern_detector,
    service_container_analyzer,
    laravel_middleware_analyzer,
    api_route_analyzer,
    rest_compliance_checker,
)


def handle_architecture_quality_routes(user_input: str, text: str, clean_text: str):
    routes = {
        "refactor planner": refactor_planner,
        "architecture consistency checker": architecture_consistency_checker,
        "naming convention analyzer": naming_convention_analyzer,
        "solid principle analyzer": solid_principle_analyzer,
        "clean code scorer": clean_code_scorer,
        "design pattern detector": design_pattern_detector,
        "service container analyzer": service_container_analyzer,
        "laravel middleware analyzer": laravel_middleware_analyzer,
        "api route analyzer": api_route_analyzer,
        "rest compliance checker": rest_compliance_checker,
    }

    handler = routes.get(text)
    if handler:
        return handler()

    return None
