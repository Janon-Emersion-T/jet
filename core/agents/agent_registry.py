from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class AgentProfile:
    key: str
    name: str
    title: str
    universe: str
    department: str
    objective: str
    route_names: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    intents: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    safety_note: Optional[str] = None


AGENTS: Dict[str, AgentProfile] = {
    # Core brain / leadership
    "jarvis": AgentProfile(
        key="jarvis",
        name="Jarvis",
        title="Central Orchestrator",
        universe="Marvel",
        department="core",
        objective="Routes requests to the correct specialist and keeps the system coordinated.",
        route_names=["basic", "task"],
        domains=["general", "productivity"],
        intents=["general", "conversation", "task"],
        keywords=["jarvis", "assistant", "help", "command"],
    ),

    "tony": AgentProfile(
        key="tony",
        name="Tony",
        title="System Architect",
        universe="Marvel",
        department="architecture",
        objective="Designs applications, product architecture, technical strategy, and advanced builds.",
        route_names=["project_analyzer", "framework", "advanced_laravel", "architecture_quality"],
        domains=["development", "project"],
        intents=["project_analysis", "framework", "laravel"],
        keywords=["architecture", "system design", "project", "application", "build app", "software"],
    ),

    "steve": AgentProfile(
        key="steve",
        name="Steve",
        title="Governance & Safety Officer",
        universe="Marvel",
        department="governance",
        objective="Handles rules, approvals, safety gates, discipline, and permission control.",
        route_names=["operator", "system_mode"],
        domains=["safety", "governance"],
        intents=["operator", "system_mode"],
        keywords=["permission", "approval", "dangerous", "safety", "policy", "confirm"],
        safety_note="Steve should be involved before destructive, external, financial, or irreversible actions.",
    ),

    # Development team
    "peter": AgentProfile(
        key="peter",
        name="Peter",
        title="Frontend Developer",
        universe="Marvel",
        department="frontend",
        objective="Builds UI, frontend components, HTML, CSS, Tailwind, React, responsive layouts, and user interfaces.",
        route_names=["html_knowledge", "css_knowledge", "frontend_platform", "frontend_quality"],
        domains=["frontend"],
        intents=["frontend", "html_knowledge", "css_knowledge", "frontend_html", "frontend_css"],
        keywords=["html", "css", "tailwind", "react", "frontend", "ui", "component", "responsive"],
    ),

    "shuri": AgentProfile(
        key="shuri",
        name="Shuri",
        title="Advanced Engineering Specialist",
        universe="Marvel",
        department="engineering",
        objective="Handles AI features, automation, integrations, experimental engineering, and complex logic.",
        route_names=["integration", "browser", "vector_memory"],
        domains=["development", "research"],
        intents=["integration", "browser", "vector_memory"],
        keywords=["ai", "automation", "integration", "api", "advanced", "experimental"],
    ),

    "thor": AgentProfile(
        key="thor",
        name="Thor",
        title="Infrastructure & DevOps Engineer",
        universe="Marvel",
        department="devops",
        objective="Handles servers, hosting, deployment, DNS, Linux administration, Docker, and uptime.",
        route_names=["dev_ops", "deployment_docs", "hosting_dns", "linux_admin", "live_environment"],
        domains=["devops", "system"],
        intents=["dev_ops", "deployment", "hosting", "linux"],
        keywords=["server", "deploy", "hosting", "dns", "linux", "nginx", "apache", "docker", "ssl"],
    ),

    "clint": AgentProfile(
        key="clint",
        name="Clint",
        title="Debugging & QA Specialist",
        universe="Marvel",
        department="quality",
        objective="Finds bugs, audits code, checks quality, validates fixes, and targets problems precisely.",
        route_names=["bug_severity", "project_health", "patch", "execution"],
        domains=["development"],
        intents=["bug", "patch", "execution"],
        keywords=["bug", "error", "fix", "traceback", "debug", "qa", "test", "issue"],
        safety_note="Execution routes may require Steve approval depending on the action.",
    ),

    "bruce": AgentProfile(
        key="bruce",
        name="Bruce",
        title="Research & Analysis Scientist",
        universe="Marvel",
        department="research",
        objective="Performs deep research, document analysis, technical investigation, and reasoning-heavy tasks.",
        route_names=["document_reader", "knowledge_academic"],
        domains=["research", "documents"],
        intents=["document", "research"],
        keywords=["research", "paper", "study", "analyze", "document", "summarize", "explain"],
    ),

    # Medical / health
    "christine": AgentProfile(
        key="christine",
        name="Christine",
        title="Medical Guidance Specialist",
        universe="Marvel",
        department="medical",
        objective="Answers general health questions, explains symptoms, gives safe next-step guidance, and warns when medical care is needed.",
        route_names=["medical"],
        domains=["medical", "health"],
        intents=["medical", "health"],
        keywords=[
            "medical", "health", "doctor", "symptom", "pain", "fever", "medicine", "injury",
            "ankle", "fissure", "blood", "infection", "hospital", "clinic", "treatment"
        ],
        safety_note="Christine provides educational guidance only and must not replace a licensed doctor.",
    ),

    "strange": AgentProfile(
        key="strange",
        name="Strange",
        title="Diagnostic Reasoning Consultant",
        universe="Marvel",
        department="medical",
        objective="Helps reason through complex symptoms, risk signals, differential possibilities, and escalation decisions.",
        route_names=["medical"],
        domains=["medical", "health"],
        intents=["medical", "health"],
        keywords=["diagnosis", "serious", "emergency", "risk", "symptoms", "condition", "complication"],
        safety_note="Strange should escalate emergency symptoms clearly and avoid pretending to diagnose.",
    ),

    # Business / marketing
    "vision": AgentProfile(
        key="vision",
        name="Vision",
        title="SEO Intelligence Specialist",
        universe="Marvel",
        department="marketing",
        objective="Handles SEO audits, structured data, indexing, technical SEO, page quality, and ranking strategy.",
        route_names=["website_audit", "frontend_quality", "marketing_analytics"],
        domains=["website", "marketing"],
        intents=["website_audit", "frontend_quality"],
        keywords=["seo", "ranking", "metadata", "schema", "sitemap", "robots", "indexing", "search console"],
    ),

    "natasha": AgentProfile(
        key="natasha",
        name="Natasha",
        title="Social Media & Communication Strategist",
        universe="Marvel",
        department="marketing",
        objective="Creates captions, campaigns, outreach messages, social media strategy, and brand communication.",
        route_names=["content_assistant", "social_planner", "business_growth"],
        domains=["marketing", "business"],
        intents=["content", "social"],
        keywords=["caption", "post", "campaign", "facebook", "instagram", "linkedin", "tiktok", "content"],
    ),

    "tchalla": AgentProfile(
        key="tchalla",
        name="TChalla",
        title="Executive Strategy Advisor",
        universe="Marvel",
        department="business",
        objective="Handles business strategy, leadership decisions, premium positioning, and company growth.",
        route_names=["business_growth", "crm"],
        domains=["business"],
        intents=["crm", "business"],
        keywords=["business", "strategy", "growth", "client", "lead", "sales", "proposal", "brand"],
    ),

    "rhodey": AgentProfile(
        key="rhodey",
        name="Rhodey",
        title="Operations Controller",
        universe="Marvel",
        department="operations",
        objective="Handles process, admin control, operational discipline, and execution tracking.",
        route_names=["employee_task_tracker", "internal_helpdesk", "ticket_prioritization"],
        domains=["hr", "operations"],
        intents=["employee_task", "helpdesk"],
        keywords=["operation", "staff", "task", "ticket", "process", "admin"],
    ),

    # Finance / accounting
    "pepper": AgentProfile(
        key="pepper",
        name="Pepper",
        title="Finance & Administration Executive",
        universe="Marvel",
        department="finance",
        objective="Handles financial reports, invoices, payroll, expenses, tax calculations, and administrative finance.",
        route_names=[
            "finance_report",
            "accounting_anomaly",
            "invoice_ocr",
            "receipt_parser",
            "tax_calculation",
            "payroll_assistant",
        ],
        domains=["finance", "accounting"],
        intents=["finance", "accounting_anomaly", "invoice", "receipt", "tax"],
        keywords=["finance", "invoice", "receipt", "tax", "payroll", "expense", "profit", "loss", "accounting"],
    ),

    # Creative
    "wanda": AgentProfile(
        key="wanda",
        name="Wanda",
        title="Creative Design Specialist",
        universe="Marvel",
        department="creative",
        objective="Creates image prompts, branding concepts, ad visuals, design direction, and creative campaigns.",
        route_names=["image_generation"],
        domains=["creative"],
        intents=["image_generation", "creative_image"],
        keywords=["image", "photo", "logo", "poster", "creative", "design", "branding", "visual"],
    ),

    "rocket": AgentProfile(
        key="rocket",
        name="Rocket",
        title="Tooling & Integration Builder",
        universe="Marvel",
        department="tools",
        objective="Builds utilities, scripts, integrations, scrapers, automation tools, and quick technical solutions.",
        route_names=["integration", "execution", "patch"],
        domains=["development", "system"],
        intents=["integration", "execution", "patch"],
        keywords=["tool", "script", "automation", "utility", "command", "terminal"],
    ),

    "groot": AgentProfile(
        key="groot",
        name="Groot",
        title="Memory Keeper",
        universe="Marvel",
        department="memory",
        objective="Stores, recalls, and protects long-term memory and personal context.",
        route_names=["memory", "vector_memory", "project_context"],
        domains=["memory", "project"],
        intents=["memory", "vector_memory", "project_context"],
        keywords=["remember", "recall", "memory", "save this", "project context"],
    ),

    # Security / risk
    "bucky": AgentProfile(
        key="bucky",
        name="Bucky",
        title="Security & Incident Response Specialist",
        universe="Marvel",
        department="security",
        objective="Handles security checks, suspicious behavior, incident response, hardening, and defensive review.",
        route_names=["bug_severity", "linux_admin", "operator"],
        domains=["security", "system"],
        intents=["security", "operator"],
        keywords=["security", "hack", "malware", "breach", "attack", "vulnerability", "incident"],
        safety_note="Bucky must stay defensive. Offensive misuse should be blocked by Steve.",
    ),

    "loki": AgentProfile(
        key="loki",
        name="Loki",
        title="Red-Team Thinking Specialist",
        universe="Marvel",
        department="security",
        objective="Finds weak points, tests assumptions, and stress-tests plans without performing harmful actions.",
        route_names=["architecture_quality", "bug_severity"],
        domains=["security", "development"],
        intents=["security", "bug"],
        keywords=["red team", "weakness", "loophole", "risk", "exploit", "test security"],
        safety_note="Loki is for safe defensive testing only, not malicious exploitation.",
    ),

    # DC / other heroes
    "barry": AgentProfile(
        key="barry",
        name="Barry",
        title="Speed & Quick Response Specialist",
        universe="DC",
        department="productivity",
        objective="Handles quick answers, summaries, fast routing, and lightweight tasks.",
        route_names=["basic", "task"],
        domains=["general", "productivity"],
        intents=["general", "task"],
        keywords=["quick", "fast", "short", "summarize", "define"],
    ),

    "oliver": AgentProfile(
        key="oliver",
        name="Oliver",
        title="Precision Planning Specialist",
        universe="DC",
        department="planning",
        objective="Handles tactical planning, checklists, action plans, and disciplined execution.",
        route_names=["task", "project_context", "business_growth"],
        domains=["productivity", "business"],
        intents=["task", "project_context"],
        keywords=["plan", "checklist", "steps", "execute", "target", "goal"],
    ),

    "bruce_wayne": AgentProfile(
        key="bruce_wayne",
        name="BruceWayne",
        title="Strategic Investigation Specialist",
        universe="DC",
        department="investigation",
        objective="Investigates complex problems, compares evidence, and builds careful strategic conclusions.",
        route_names=["research", "document_reader", "project_analyzer"],
        domains=["research", "business", "development"],
        intents=["research", "document", "project_analysis"],
        keywords=["investigate", "compare", "evidence", "strategy", "case", "deep check"],
    ),

    "clark": AgentProfile(
        key="clark",
        name="Clark",
        title="Public Communication Specialist",
        universe="DC",
        department="communication",
        objective="Writes formal, public-facing, trustworthy announcements, letters, articles, and statements.",
        route_names=["content_assistant", "report_export"],
        domains=["marketing", "documents"],
        intents=["content", "report"],
        keywords=["letter", "article", "announcement", "statement", "press", "public"],
    ),
}


DEFAULT_AGENT_KEY = "jarvis"


def get_agent(agent_key: str) -> AgentProfile:
    return AGENTS.get(agent_key, AGENTS[DEFAULT_AGENT_KEY])


def list_agents() -> List[AgentProfile]:
    return list(AGENTS.values())


def find_agent_by_route(route_name: str) -> AgentProfile:
    route_name = (route_name or "").strip().lower()

    for agent in AGENTS.values():
        if route_name in [name.lower() for name in agent.route_names]:
            return agent

    return AGENTS[DEFAULT_AGENT_KEY]


def resolve_agent(
    route_name: Optional[str] = None,
    domain: Optional[str] = None,
    intent: Optional[str] = None,
    text: Optional[str] = None,
) -> AgentProfile:
    route_name = (route_name or "").strip().lower()
    domain = (domain or "").strip().lower()
    intent = (intent or "").strip().lower()
    text = (text or "").strip().lower()

    # 1. Exact route match is strongest.
    if route_name:
        for agent in AGENTS.values():
            if route_name in [name.lower() for name in agent.route_names]:
                return agent

    # 2. Intent match.
    if intent:
        for agent in AGENTS.values():
            if intent in [item.lower() for item in agent.intents]:
                return agent

    # 3. Keyword match.
    if text:
        best_agent = None
        best_score = 0

        for agent in AGENTS.values():
            score = sum(1 for keyword in agent.keywords if keyword.lower() in text)

            if score > best_score:
                best_score = score
                best_agent = agent

        if best_agent and best_score > 0:
            return best_agent

    # 4. Domain match.
    if domain:
        for agent in AGENTS.values():
            if domain in [item.lower() for item in agent.domains]:
                return agent

    return AGENTS[DEFAULT_AGENT_KEY]


def format_agent_intro(agent: AgentProfile) -> str:
    return f"{agent.name} — {agent.title}"


def format_agent_response(agent: AgentProfile, response: str) -> str:
    if not response:
        return response

    header = f"[{agent.name} | {agent.title}]"

    if response.startswith("["):
        return response

    if agent.safety_note:
        return f"{header}\n{response}\n\nNote: {agent.safety_note}"

    return f"{header}\n{response}"
