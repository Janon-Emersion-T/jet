from tools.linux_admin_tools import (
    window_manager,
    linux_system_monitor,
    disk_cleanup_assistant,
    log_cleanup_assistant,
    service_status_checker,
    nginx_config_checker,
    php_fpm_checker,
    mysql_checker,
    laravel_deployment_checker,
    github_actions_helper,
    linux_admin_help,
)


def handle_linux_admin_routes(user_input: str, text: str, clean_text: str):
    if text in ["linux admin help", "system admin help", "admin tools help"]:
        return linux_admin_help()

    if text in ["window manager", "window manager status"]:
        return window_manager()

    if text in ["linux system monitor", "system monitor", "linux monitor"]:
        return linux_system_monitor()

    if text in ["disk cleanup assistant", "disk cleanup"]:
        return disk_cleanup_assistant()

    if text in ["log cleanup assistant", "log cleanup"]:
        return log_cleanup_assistant()

    if text == "service status checker":
        return service_status_checker()

    if text.startswith("service status checker "):
        service = user_input.replace("service status checker ", "", 1).strip()
        return service_status_checker(service)

    if text in ["nginx config checker", "check nginx config"]:
        return nginx_config_checker()

    if text in ["php fpm checker", "php-fpm checker", "check php fpm"]:
        return php_fpm_checker()

    if text in ["mysql checker", "check mysql"]:
        return mysql_checker()

    if text in ["laravel deployment checker", "check laravel deployment"]:
        return laravel_deployment_checker()

    if text in ["github actions helper", "actions helper"]:
        return github_actions_helper()

    return None
