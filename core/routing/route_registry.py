from core.routing.route_contracts import RouteModule

from core.routes.html_knowledge_routes import handle_html_knowledge_routes
from core.routes.css_knowledge_routes import handle_css_knowledge_routes

from core.routes.image_generation_routes import handle_image_generation_routes
from core.routes.nlp_test_routes import handle_nlp_test_routes
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
from core.routes.invoice_ocr_routes import handle_invoice_ocr_routes
from core.routes.receipt_parser_routes import handle_receipt_parser_routes
from core.routes.tax_calculation_routes import handle_tax_calculation_routes
from core.routes.payroll_assistant_routes import handle_payroll_assistant_routes
from core.routes.hr_onboarding_routes import handle_hr_onboarding_routes
from core.routes.employee_task_tracker_routes import handle_employee_task_tracker_routes
from core.routes.attendance_assistant_routes import handle_attendance_assistant_routes
from core.routes.internal_helpdesk_routes import handle_internal_helpdesk_routes
from core.routes.ticket_prioritization_routes import handle_ticket_prioritization_routes
from core.routes.bug_severity_routes import handle_bug_severity_routes


ROUTE_MODULES = [
    RouteModule(
        name="html_knowledge",
        domain="frontend",
        handler=handle_html_knowledge_routes,
        description="Learn, update, explain, audit, and generate practical HTML knowledge.",
        keywords=[
            "html",
            "doctype",
            "tag",
            "element",
            "semantic",
            "accessibility",
            "form",
            "meta",
            "head",
            "body",
            "section",
            "article",
            "landing page",
            "website structure",
            "web page",
            "frontend markup",

            # Natural language learning/status phrases
            "know html",
            "already know html",
            "check html knowledge",
            "html knowledge",
            "latest html",
            "official html",
            "official sources",
            "html living standard",
            "whatwg",
            "mdn",
            "learn html",
            "teach yourself html",

            # Natural language audit phrases
            "html file",
            "sample html",
            "sample html file",
            "audit html",
            "validate html",
            "check html file",
            "written properly",
            "production ready",
            "html audit",

            # Natural language generation phrases
            "clean html foundation",
            "basic structure",
            "professional website",
            "company landing page",
            "website foundation",
            "html foundation",
        ],
        intents=[
            "html_knowledge",
            "frontend_html",
            "learn_html",
            "audit_html",
            "generate_html",
            "explain_html",
            "frontend",
            "command",
        ],
        canonical_commands=[
            "update html knowledge",
            "html knowledge status",
            "check html knowledge",
            "check whether you already know html",
            "html blueprint",
            "create html starter",
            "audit html file",
            "explain html element",
        ],
        examples=[
            "teach yourself latest HTML",
            "learn HTML properly",
            "check whether you already know HTML",
            "what HTML knowledge do you have",
            "create a semantic HTML page",
            "audit this HTML file",
            "audit my sample HTML file",
            "check whether my HTML file is production ready",
            "check whether test_documents/sample.html is written properly",
            "explain section tag",
            "make a landing page structure",
            "give me a clean HTML foundation",
        ],
    ),

    RouteModule(
        name="css_knowledge",
        domain="frontend",
        handler=handle_css_knowledge_routes,
        description="Learn, update, explain, audit, and generate practical CSS knowledge.",
        keywords=[
            "css",
            "stylesheet",
            "style sheet",
            "styles",
            "style",
            "selector",
            "specificity",
            "cascade",
            "inheritance",
            "box model",
            "display",
            "position",
            "flex",
            "flexbox",
            "grid",
            "subgrid",
            "media query",
            "media queries",
            "container query",
            "container queries",
            "responsive css",
            "responsive design",
            "custom properties",
            "css variables",
            "design tokens",
            "css architecture",
            "css foundation",
            "modern css",
            "css nesting",
            "cascade layers",
            "color-mix",
            "logical properties",
            "view transitions",

            # Natural language learning/status phrases
            "know css",
            "already know css",
            "check css knowledge",
            "css knowledge",
            "latest css",
            "official css",
            "official sources",
            "w3c css",
            "mdn css",
            "css snapshot",
            "learn css",
            "teach yourself css",

            # Natural language audit phrases
            "css file",
            "sample css",
            "sample stylesheet",
            "audit css",
            "validate css",
            "check css file",
            "production ready css",
            "css audit",

            # Natural language generation phrases
            "clean css foundation",
            "base css",
            "starter css",
            "professional stylesheet",
            "website style",
            "landing page style",
        ],
        intents=[
            "css_knowledge",
            "frontend_css",
            "learn_css",
            "audit_css",
            "generate_css",
            "explain_css",
            "frontend",
            "command",
        ],
        canonical_commands=[
            "update css knowledge",
            "css knowledge status",
            "check css knowledge",
            "check whether you already know css",
            "css blueprint",
            "create css starter",
            "audit css file",
            "explain css",
            "translate css",
        ],
        examples=[
            "teach yourself latest CSS",
            "learn CSS properly",
            "check whether you already know CSS",
            "what CSS knowledge do you have",
            "create a modern CSS foundation",
            "audit this CSS file",
            "audit my sample CSS file",
            "check whether resources/css/app.css is production ready",
            "explain CSS cascade",
            "explain container queries",
            "explain CSS specificity",
            "translate this CSS to Tailwind",
            "make a responsive landing page style",
        ],
    ),

    RouteModule(
        name="image_generation",
        domain="creative",
        handler=handle_image_generation_routes,
        description="Generate image prompts and manage image creation workflows.",
        keywords=["image", "photo", "picture", "poster", "logo", "favicon", "realistic", "generate"],
        intents=["image_generation", "creative_image"],
        examples=["create an image", "generate a realistic ad image", "make a logo"],
    ),

    RouteModule(
        name="nlp_test",
        domain="diagnostics",
        handler=handle_nlp_test_routes,
        description="Test and inspect NLP understanding.",
        keywords=["test nlp", "analyze command", "nlp memory", "followup"],
        intents=["nlp_test", "diagnostic"],
        examples=["test nlp create html page", "analyze command update html"],
    ),

    RouteModule(
        name="project_context",
        domain="project",
        handler=handle_project_context_routes,
        description="Manage project context and project-specific memory.",
        keywords=["project context", "current project", "remember this project"],
        intents=["project_context"],
    ),

    RouteModule(
        name="project_analyzer",
        domain="development",
        handler=handle_project_analyzer_routes,
        description="Analyze project files, code structure, and implementation health.",
        keywords=["analyze project", "check repo", "scan project", "project structure"],
        intents=["project_analysis"],
    ),

    RouteModule(
        name="dev_ops",
        domain="development",
        handler=handle_dev_ops_routes,
        description="Handle development operations, Git, deployment, and environment tasks.",
        keywords=["git", "deploy", "server", "pipeline", "env", "docker", "hosting"],
        intents=["dev_ops"],
    ),

    RouteModule(
        name="framework",
        domain="development",
        handler=handle_framework_routes,
        description="Handle framework-specific development such as Laravel, React, Blade, Vue, and Next.js.",
        keywords=["laravel", "react", "vue", "next", "blade", "livewire", "tailwind", "framework"],
        intents=["framework"],
    ),

    RouteModule(
        name="frontend_platform",
        domain="frontend",
        handler=handle_frontend_platform_routes,
        description="Handle frontend platform tasks.",
        keywords=["frontend", "ui", "layout", "component", "responsive", "tailwind", "css"],
        intents=["frontend"],
    ),

    RouteModule(
        name="frontend_quality",
        domain="frontend",
        handler=handle_frontend_quality_routes,
        description="Audit frontend quality, responsiveness, accessibility, SEO, and UX.",
        keywords=["frontend quality", "responsive", "accessibility", "ux", "ui audit", "seo html"],
        intents=["frontend_quality"],
    ),

    RouteModule(
        name="advanced_laravel",
        domain="development",
        handler=handle_advanced_laravel_routes,
        description="Handle advanced Laravel implementation.",
        keywords=["laravel", "migration", "controller", "model", "route", "blade", "livewire", "filament"],
        intents=["laravel"],
    ),

    RouteModule(
        name="database_intelligence",
        domain="database",
        handler=handle_database_intelligence_routes,
        description="Analyze and design database structures.",
        keywords=["database", "mysql", "migration", "schema", "table", "relationship", "sql"],
        intents=["database"],
    ),

    RouteModule(
        name="patch",
        domain="development",
        handler=handle_patch_routes,
        description="Create, show, apply, and reject code patches.",
        keywords=["patch", "proposal", "apply changes", "modify file", "fix code"],
        intents=["patch"],
        safety_level="write",
    ),

    RouteModule(
        name="execution",
        domain="system",
        handler=handle_execution_routes,
        description="Execute terminal/system commands when allowed.",
        keywords=["run command", "terminal", "execute", "shell"],
        intents=["execution"],
        safety_level="dangerous",
    ),

    RouteModule(
        name="backup",
        domain="system",
        handler=handle_backup_routes,
        description="Backup project files and important data.",
        keywords=["backup", "restore", "snapshot"],
        intents=["backup"],
        safety_level="write",
    ),

    RouteModule(
        name="email",
        domain="communication",
        handler=handle_email_routes,
        description="Handle email creation, reading, drafting, and sending.",
        keywords=["email", "mail", "gmail", "send", "draft", "inbox"],
        intents=["email"],
        safety_level="external_action",
    ),

    RouteModule(
        name="document_reader",
        domain="documents",
        handler=handle_document_reader_routes,
        description="Read and summarize documents.",
        keywords=["document", "pdf", "docx", "read file", "summarize file"],
        intents=["document"],
    ),

    RouteModule(
        name="spreadsheet_analysis",
        domain="documents",
        handler=handle_spreadsheet_analysis_routes,
        description="Analyze spreadsheets and tabular data.",
        keywords=["spreadsheet", "excel", "csv", "xlsx", "sheet"],
        intents=["spreadsheet"],
    ),

    RouteModule(
        name="report_export",
        domain="documents",
        handler=handle_report_export_routes,
        description="Export reports.",
        keywords=["report", "export report", "pdf report"],
        intents=["report"],
    ),

    RouteModule(
        name="powerpoint_export",
        domain="documents",
        handler=handle_powerpoint_export_routes,
        description="Create and export presentations.",
        keywords=["powerpoint", "ppt", "slides", "presentation"],
        intents=["presentation"],
    ),

    RouteModule(
        name="browser",
        domain="research",
        handler=handle_browser_routes,
        description="Browse or inspect web pages.",
        keywords=["browse", "open website", "search web", "internet", "website"],
        intents=["browser"],
    ),

    RouteModule(
        name="website_audit",
        domain="website",
        handler=handle_website_audit_routes,
        description="Audit websites for SEO, structure, performance, and quality.",
        keywords=["audit website", "seo audit", "check website", "website audit"],
        intents=["website_audit"],
    ),

    RouteModule(
        name="content_assistant",
        domain="marketing",
        handler=handle_content_assistant_routes,
        description="Create content, captions, blogs, and marketing copy.",
        keywords=["content", "caption", "blog", "copywriting", "post"],
        intents=["content"],
    ),

    RouteModule(
        name="social_planner",
        domain="marketing",
        handler=handle_social_planner_routes,
        description="Plan social media content and schedules.",
        keywords=["social media", "facebook", "instagram", "linkedin", "tiktok", "post schedule"],
        intents=["social"],
    ),

    RouteModule(
        name="crm",
        domain="business",
        handler=handle_crm_routes,
        description="Handle customers, leads, CRM notes, and sales workflow.",
        keywords=["customer", "lead", "crm", "client", "sales"],
        intents=["crm"],
    ),

    RouteModule(
        name="finance_report",
        domain="finance",
        handler=handle_financial_report_routes,
        description="Create and analyze finance reports.",
        keywords=["finance", "financial report", "profit", "loss", "income", "expense"],
        intents=["finance"],
    ),

    RouteModule(
        name="accounting_anomaly",
        domain="finance",
        handler=handle_accounting_anomaly_routes,
        description="Detect accounting anomalies.",
        keywords=["anomaly", "accounting issue", "not tally", "mismatch"],
        intents=["accounting_anomaly"],
    ),

    RouteModule(
        name="invoice_ocr",
        domain="finance",
        handler=handle_invoice_ocr_routes,
        description="Read invoices using OCR or parsing.",
        keywords=["invoice", "ocr invoice", "bill"],
        intents=["invoice"],
    ),

    RouteModule(
        name="receipt_parser",
        domain="finance",
        handler=handle_receipt_parser_routes,
        description="Parse receipts.",
        keywords=["receipt", "parse receipt", "expense receipt"],
        intents=["receipt"],
    ),

    RouteModule(
        name="tax_calculation",
        domain="finance",
        handler=handle_tax_calculation_routes,
        description="Calculate taxes.",
        keywords=["tax", "vat", "calculation"],
        intents=["tax"],
    ),

    RouteModule(
        name="hr_onboarding",
        domain="hr",
        handler=handle_hr_onboarding_routes,
        description="Handle HR onboarding.",
        keywords=["hr", "onboarding", "employee", "staff joining"],
        intents=["hr"],
    ),

    RouteModule(
        name="employee_task_tracker",
        domain="hr",
        handler=handle_employee_task_tracker_routes,
        description="Track employee tasks.",
        keywords=["employee task", "staff task", "task tracker"],
        intents=["employee_task"],
    ),

    RouteModule(
        name="attendance",
        domain="hr",
        handler=handle_attendance_assistant_routes,
        description="Handle attendance-related tasks.",
        keywords=["attendance", "leave", "present", "absent"],
        intents=["attendance"],
    ),

    RouteModule(
        name="memory",
        domain="memory",
        handler=handle_memory_routes,
        description="Store and retrieve memory.",
        keywords=["remember", "memory", "recall", "save this"],
        intents=["memory"],
    ),

    RouteModule(
        name="vector_memory",
        domain="memory",
        handler=handle_vector_memory_routes,
        description="Search and manage vector memory.",
        keywords=["vector memory", "knowledge memory", "semantic memory"],
        intents=["vector_memory"],
    ),

    RouteModule(
        name="task",
        domain="productivity",
        handler=handle_task_routes,
        description="Manage tasks and reminders.",
        keywords=["help", "hello", "hi", "good morning", "good evening"],
        intents=["task"],
    ),

    RouteModule(
        name="basic",
        domain="general",
        handler=handle_basic_routes,
        description="General/basic conversation handler.",
        keywords=[
            "help",
            "hello",
            "hi",
            "hey",
            "status",
            "location",
            "weather",
            "forecast",
            "temperature",
            "rain",
            "calendar",
            "calender",
            "schedule",
            "email",
            "gmail",
            "inbox",
        ],
        intents=[
            "general",
            "conversation",
            "small_talk",
            "location",
            "weather",
            "calendar",
            "email",
        ],
        requires_intent_arg=True,
    ),
]


def get_route_modules():
    return ROUTE_MODULES


def get_route_module_by_name(name: str):
    for module in ROUTE_MODULES:
        if module.name == name:
            return module
    return None
