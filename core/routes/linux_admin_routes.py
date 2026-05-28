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
from tools.vps_monitoring_tools import vps_monitoring_engine
from tools.infrastructure_monitoring_tools import (
    cpu_ram_monitoring_assistant,
    disk_health_checker,
    service_auto_recovery_planner,
    uptime_monitoring_assistant,
    backup_verification_engine,
    disaster_recovery_planner,
    infrastructure_topology_mapper,
    network_scanner,
)
from tools.ai_infrastructure_tools import (
    port_monitoring_assistant,
    local_ai_cluster_planner,
    gpu_utilization_assistant,
    cuda_setup_advisor,
    ollama_optimization_assistant,
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

    if text in ["vps monitoring engine", "vps monitor", "check vps health", "monitor my server"]:
        return vps_monitoring_engine()

    if text in ["367 help", "phase 367 help", "vps monitoring help"]:
        return (
            "VPS MONITORING ENGINE COMMANDS - PHASE 367\n\n"
            "vps monitoring engine\n"
            "check vps health\n"
            "monitor my server"
        )

    if text in ["cpu ram monitoring assistant", "cpu/ram monitoring assistant", "check cpu ram", "monitor cpu ram"]:
        return cpu_ram_monitoring_assistant()

    if text in ["disk health checker", "check disk health", "disk health"]:
        return disk_health_checker()

    if text in ["service auto-recovery planner", "service auto recovery planner", "plan service recovery"]:
        return service_auto_recovery_planner()

    if text in ["uptime monitoring assistant", "check uptime", "uptime monitor"]:
        return uptime_monitoring_assistant()

    if text in ["backup verification engine", "verify backups", "check backups"]:
        return backup_verification_engine()

    if text in ["disaster recovery planner", "plan disaster recovery", "check disaster recovery"]:
        return disaster_recovery_planner()

    if text in ["infrastructure topology mapper", "map infrastructure", "show infrastructure topology"]:
        return infrastructure_topology_mapper()

    if text in ["network scanner", "scan local network listeners", "check listening ports"]:
        return network_scanner()

    if text in ["368 help", "phase 368 help", "cpu ram help"]:
        return "CPU/RAM MONITORING ASSISTANT COMMANDS - PHASE 368\n\ncpu ram monitoring assistant\ncheck cpu ram\nmonitor cpu ram"

    if text in ["369 help", "phase 369 help", "disk health help"]:
        return "DISK HEALTH CHECKER COMMANDS - PHASE 369\n\ndisk health checker\ncheck disk health"

    if text in ["370 help", "phase 370 help", "service recovery help"]:
        return "SERVICE AUTO-RECOVERY PLANNER COMMANDS - PHASE 370\n\nservice auto-recovery planner\nplan service recovery"

    if text in ["371 help", "phase 371 help", "uptime help"]:
        return "UPTIME MONITORING ASSISTANT COMMANDS - PHASE 371\n\nuptime monitoring assistant\ncheck uptime"

    if text in ["372 help", "phase 372 help", "backup help"]:
        return "BACKUP VERIFICATION ENGINE COMMANDS - PHASE 372\n\nbackup verification engine\nverify backups\ncheck backups"

    if text in ["373 help", "phase 373 help", "disaster recovery help"]:
        return "DISASTER RECOVERY PLANNER COMMANDS - PHASE 373\n\ndisaster recovery planner\nplan disaster recovery"

    if text in ["374 help", "phase 374 help", "topology help"]:
        return "INFRASTRUCTURE TOPOLOGY MAPPER COMMANDS - PHASE 374\n\ninfrastructure topology mapper\nmap infrastructure"

    if text in ["375 help", "phase 375 help", "network scanner help"]:
        return "NETWORK SCANNER COMMANDS - PHASE 375\n\nnetwork scanner\ncheck listening ports"

    if text in ["port monitoring assistant", "monitor ports", "check port monitoring"]:
        return port_monitoring_assistant()

    if text in ["local ai cluster planner", "plan local ai cluster", "ai cluster planner"]:
        return local_ai_cluster_planner()

    if text in ["gpu utilization assistant", "check gpu utilization", "gpu monitor"]:
        return gpu_utilization_assistant()

    if text in ["cuda setup advisor", "check cuda setup", "cuda advisor"]:
        return cuda_setup_advisor()

    if text in ["ollama optimization assistant", "optimize ollama", "ollama advisor"]:
        return ollama_optimization_assistant()

    if text in ["376 help", "phase 376 help", "port monitoring help"]:
        return "PORT MONITORING ASSISTANT COMMANDS - PHASE 376\n\nport monitoring assistant\nmonitor ports"

    if text in ["377 help", "phase 377 help", "ai cluster help"]:
        return "LOCAL AI CLUSTER PLANNER COMMANDS - PHASE 377\n\nlocal ai cluster planner\nplan local ai cluster"

    if text in ["378 help", "phase 378 help", "gpu help"]:
        return "GPU UTILIZATION ASSISTANT COMMANDS - PHASE 378\n\ngpu utilization assistant\ncheck gpu utilization"

    if text in ["379 help", "phase 379 help", "cuda help"]:
        return "CUDA SETUP ADVISOR COMMANDS - PHASE 379\n\ncuda setup advisor\ncheck cuda setup"

    if text in ["380 help", "phase 380 help", "ollama help"]:
        return "OLLAMA OPTIMIZATION ASSISTANT COMMANDS - PHASE 380\n\nollama optimization assistant\noptimize ollama"

    return None
