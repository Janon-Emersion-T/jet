from tools.deployment_docs_tools import (
    swagger_openapi_generator,
    readme_auto_generator,
    project_onboarding_assistant,
    developer_environment_checker,
    linux_package_dependency_checker,
    docker_awareness_layer,
    shared_hosting_compatibility_checker,
    cpanel_deployment_assistant,
    hostinger_deployment_assistant,
    nginx_virtual_host_generator,
)


def handle_deployment_docs_routes(user_input: str, text: str, clean_text: str):
    if text in ["swagger generator", "openapi generator", "swagger openapi generator"]:
        return swagger_openapi_generator()

    if text in ["readme generator", "readme auto generator", "generate readme"]:
        return readme_auto_generator()

    if text in ["project onboarding assistant", "onboarding assistant", "onboard project"]:
        return project_onboarding_assistant()

    if text in ["developer environment checker", "dev environment checker", "environment checker"]:
        return developer_environment_checker()

    if text in ["linux package dependency checker", "linux dependency checker", "package dependency checker"]:
        return linux_package_dependency_checker()

    if text in ["docker awareness layer", "docker checker", "docker awareness"]:
        return docker_awareness_layer()

    if text in ["shared hosting checker", "shared hosting compatibility checker"]:
        return shared_hosting_compatibility_checker()

    if text in ["cpanel deployment assistant", "cpanel assistant"]:
        return cpanel_deployment_assistant()

    if text in ["hostinger deployment assistant", "hostinger assistant"]:
        return hostinger_deployment_assistant()

    if text.startswith("nginx virtual host generator"):
        domain = text.replace("nginx virtual host generator", "").strip()
        return nginx_virtual_host_generator(domain)

    if text in ["deployment docs help", "251 260 help", "phases 251 260"]:
        return """DEPLOYMENT / DOCUMENTATION COMMANDS — PHASES 251–260

251. swagger openapi generator
252. readme auto generator
253. project onboarding assistant
254. developer environment checker
255. linux package dependency checker
256. docker awareness layer
257. shared hosting compatibility checker
258. cpanel deployment assistant
259. hostinger deployment assistant
260. nginx virtual host generator example.com
"""

    return None
