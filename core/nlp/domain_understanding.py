from dataclasses import dataclass
from typing import Dict, List, Optional


DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    "business": ["revenue", "strategy", "crm", "customer", "growth"],
    "developer": ["code", "bug", "function", "class", "api", "test", "laravel", "python"],
    "devops": ["deploy", "server", "docker", "nginx", "git", "ci", "logs"],
    "marketing": ["campaign", "keyword", "conversion", "analytics"],
    "accounting": ["invoice", "expense", "tax", "payroll", "ledger", "financial"],
    "research": ["research", "source", "citation", "paper", "study", "evidence"],
    "security": ["security", "vulnerability", "permission", "unsafe", "dangerous", "breach", "secret"],
    "seo": ["seo", "ranking", "search intent", "backlink", "organic"],
    "social": ["instagram", "linkedin", "tiktok", "social media", "engagement"],
    "legal": ["legal", "policy", "compliance", "contract", "privacy", "regulation"],
    "design": ["ui", "ux", "design", "layout", "accessibility", "prototype"],
    "content": ["write", "story", "article", "copy", "script"],
    "sales": ["sales", "lead", "close", "pitch", "outreach"],
    "hr": ["hr", "employee", "hiring", "leave", "onboarding", "people"],
    "medical": ["medical", "symptom", "medicine", "dose", "health safety"],
    "fitness": ["fitness", "workout", "exercise", "gym", "training plan"],
    "basketball": ["basketball", "shooting", "dribble", "defense", "court"],
    "project": ["project plan", "milestone", "deadline", "roadmap", "sprint"],
    "ai": ["artificial intelligence", "machine learning", "llm", "model"],
    "nlp": ["nlp", "intent", "embedding", "language model"],
}


@dataclass
class DomainDecision:
    domain: str
    confidence: float
    matched_keywords: List[str]


def understand_domain(text: str) -> DomainDecision:
    lowered = (text or "").lower()
    scored = {
        domain: [word for word in keywords if word in lowered]
        for domain, keywords in DOMAIN_KEYWORDS.items()
    }
    domain, matches = max(scored.items(), key=lambda item: len(item[1]))
    if not matches:
        return DomainDecision("general", 0.0, [])
    return DomainDecision(domain, min(1.0, 0.45 + len(matches) * 0.16), matches)
