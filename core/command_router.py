import string

from core.intent_classifier import classify_intent
from core.ai_fallback import handle_ai_fallback

from core.routes.basic_routes import handle_basic_routes
from core.routes.memory_routes import handle_memory_routes
from core.routes.project_context_routes import handle_project_context_routes
from core.routes.project_analyzer_routes import handle_project_analyzer_routes
from core.routes.dev_ops_routes import handle_dev_ops_routes
from core.routes.framework_routes import handle_framework_routes
from core.routes.patch_routes import handle_patch_routes
from core.routes.project_health_routes import handle_project_health_routes
from core.routes.execution_routes import handle_execution_routes
from core.routes.backup_routes import handle_backup_routes
from core.routes.task_routes import handle_task_routes
from core.routes.vector_memory_routes import handle_vector_memory_routes
from core.routes.system_mode_routes import handle_system_mode_routes
from core.routes.browser_routes import handle_browser_routes
from core.routes.website_audit_routes import handle_website_audit_routes
from core.routes.content_assistant_routes import handle_content_assistant_routes
from core.routes.social_planner_routes import handle_social_planner_routes
from core.routes.crm_routes import handle_crm_routes
from core.routes.integration_routes import handle_integration_routes
from core.routes.document_reader_routes import handle_document_reader_routes
from core.routes.vision_routes import handle_vision_routes
from core.routes.desktop_control_routes import handle_desktop_control_routes
from core.routes.integration_routes import handle_integration_routes
from core.routes.vision_routes import handle_vision_routes
from core.routes.desktop_control_routes import handle_desktop_control_routes
from core.routes.linux_admin_routes import handle_linux_admin_routes
from core.routes.operator_routes import handle_operator_routes
from core.routes.architecture_quality_routes import handle_architecture_quality_routes
from core.routes.advanced_laravel_routes import handle_advanced_laravel_routes
from core.routes.database_intelligence_routes import handle_database_intelligence_routes
from core.routes.deployment_docs_routes import handle_deployment_docs_routes
from core.routes.hosting_dns_routes import handle_hosting_dns_routes
from core.routes.frontend_quality_routes import handle_frontend_quality_routes
from core.routes.frontend_platform_routes import handle_frontend_platform_routes
from core.routes.packaging_analytics_routes import handle_packaging_analytics_routes
from core.routes.marketing_analytics_routes import handle_marketing_analytics_routes
from core.routes.business_growth_routes import handle_business_growth_routes
from core.routes.email_routes import handle_email_routes
from core.routes.knowledge_academic_routes import handle_knowledge_academic_routes
from core.routes.live_environment_routes import handle_live_environment_routes
from core.routes.report_export_routes import handle_report_export_routes
from core.routes.powerpoint_export_routes import handle_powerpoint_export_routes
from core.routes.spreadsheet_analysis_routes import handle_spreadsheet_analysis_routes
from core.routes.financial_report_routes import handle_financial_report_routes
from core.routes.accounting_anomaly_routes import handle_accounting_anomaly_routes




def route_command(user_input: str) -> str:
    text = user_input.lower().strip()

    clean_text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    intent = classify_intent(user_input)

    route_handlers = [
        handle_live_environment_routes,
        handle_email_routes,
        handle_integration_routes,
        handle_vision_routes,
        handle_desktop_control_routes,
        handle_basic_routes,
        handle_memory_routes,
        handle_framework_routes,
        handle_database_intelligence_routes,
        handle_dev_ops_routes,
        handle_project_analyzer_routes,
        handle_frontend_platform_routes,
        handle_project_context_routes,
        handle_patch_routes,
        handle_project_health_routes,
        handle_report_export_routes,
        handle_powerpoint_export_routes,
        handle_spreadsheet_analysis_routes,
        handle_financial_report_routes,
        handle_accounting_anomaly_routes,
        handle_architecture_quality_routes,
        handle_execution_routes,
        handle_backup_routes,
        handle_task_routes,
        handle_vector_memory_routes,
        handle_system_mode_routes,
        handle_browser_routes,
        handle_website_audit_routes,
        handle_frontend_quality_routes,
        handle_content_assistant_routes,
        handle_social_planner_routes,
        handle_crm_routes,
        handle_integration_routes,
        handle_document_reader_routes,
        handle_vision_routes,
        handle_desktop_control_routes,
        handle_linux_admin_routes,
        handle_hosting_dns_routes,
        handle_deployment_docs_routes,
        handle_operator_routes,
        handle_advanced_laravel_routes,
        handle_packaging_analytics_routes,
        handle_marketing_analytics_routes,
        handle_business_growth_routes,
        handle_knowledge_academic_routes,
    ]

    for handler in route_handlers:
        if handler == handle_basic_routes:
            response = handler(user_input, text, clean_text, intent)
        else:
            response = handler(user_input, text, clean_text)

        if response is not None:
            return response

    return handle_ai_fallback(user_input)