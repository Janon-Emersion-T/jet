from dataclasses import dataclass
from typing import Dict, List, Optional


DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    "business": ["revenue", "strategy", "crm", "sales", "customer", "growth"],
    "developer": ["code", "bug", "function", "class", "api", "test", "laravel", "python"],
    "devops": ["deploy", "server", "docker", "nginx", "git", "ci", "logs"],
    "marketing": ["seo", "campaign", "keyword", "social", "conversion", "analytics"],
    "accounting": ["invoice", "expense", "tax", "payroll", "ledger", "financial"],
    "research": ["research", "source", "citation", "paper", "study", "evidence"],
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
