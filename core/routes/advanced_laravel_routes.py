from tools.advanced_laravel_auditors import (
    graphql_readiness_checker,
    webhook_simulator,
    queue_worker_analyzer,
    horizon_integration_assistant,
    redis_integration_checker,
    cache_strategy_advisor,
    session_handling_analyzer,
    authentication_flow_inspector,
    rbac_permission_auditor,
    multi_tenant_isolation_checker,
)


def handle_advanced_laravel_routes(user_input: str, text: str, clean_text: str):
    if text in ["graphql readiness checker", "check graphql readiness"]:
        return graphql_readiness_checker()

    if text in ["webhook simulator", "simulate webhook"]:
        return webhook_simulator()

    if text in ["queue worker analyzer", "analyze queue worker"]:
        return queue_worker_analyzer()

    if text in ["horizon integration assistant", "horizon assistant"]:
        return horizon_integration_assistant()

    if text in ["redis integration checker", "check redis"]:
        return redis_integration_checker()

    if text in ["cache strategy advisor", "cache advisor"]:
        return cache_strategy_advisor()

    if text in ["session handling analyzer", "analyze sessions"]:
        return session_handling_analyzer()

    if text in ["authentication flow inspector", "auth flow inspector"]:
        return authentication_flow_inspector()

    if text in ["rbac permission auditor", "permission auditor"]:
        return rbac_permission_auditor()

    if text in ["multi tenant isolation checker", "tenant isolation checker"]:
        return multi_tenant_isolation_checker()

    return None
