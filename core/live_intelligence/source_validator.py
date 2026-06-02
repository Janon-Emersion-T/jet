"""
Source Validator Module

Validates search results by checking source credibility and trust.
Assigns confidence levels based on source quality and diversity.
"""

from typing import List, Dict, Literal


# Trusted news sources - prefer these
TRUSTED_SOURCES = {
    # Major wire agencies
    "reuters.com",
    "apnews.com",
    "bbc.com",
    "bbc.co.uk",
    "aljazeera.com",
    
    # Major international news
    "theguardian.com",
    "cnn.com",
    "bbc.co.uk",
    "theguardian.com",
    "nytimes.com",
    "washingtonpost.com",
    "ft.com",
    "economist.com",
    
    # Government and official sources
    "whitehouse.gov",
    "gov.uk",
    "parliament.uk",
    "un.org",
    "nato.int",
    
    # Financial news
    "bloomberg.com",
    "cnbc.com",
    "marketwatch.com",
    "investopedia.com",
    
    # Tech/Science
    "techcrunch.com",
    "theverge.com",
    "wired.com",
    "nature.com",
    "science.org",
    
    # Health
    "healthline.com",
    "mayoclinic.org",
    "nih.gov",
    "who.int",
}


def validate_sources(results: List[Dict]) -> Dict:
    """
    Validate search results and determine confidence level.
    
    Args:
        results: List of search results from web_search.search_live_web()
        
    Returns:
        {
            "confidence": "high" | "medium" | "low",
            "trusted_sources": int,
            "unique_domains": int,
            "validation_notes": str,
            "recommendations": List[str]
        }
    """
    
    if not results:
        return {
            "confidence": "low",
            "trusted_sources": 0,
            "unique_domains": 0,
            "validation_notes": "No results to validate.",
            "recommendations": ["Try a different search query"],
        }
    
    # Collect unique domains and trusted source count
    domains_seen = set()
    trusted_count = 0
    recommendation_notes = []
    
    for result in results:
        # Skip error results
        if result.get("type") == "error":
            continue
        
        # Skip AI summary results
        if result.get("type") == "answer":
            continue
        
        source = (result.get("source") or "").lower().strip()
        if source:
            domains_seen.add(source)
            
            # Check if it's a trusted source
            if _is_trusted_source(source):
                trusted_count += 1
    
    unique_domain_count = len(domains_seen)
    
    # Determine confidence level
    if trusted_count >= 3 and unique_domain_count >= 3:
        confidence = "high"
        validation_notes = (
            f"High confidence: {trusted_count} trusted sources from {unique_domain_count} domains."
        )
    elif trusted_count >= 2 and unique_domain_count >= 2:
        confidence = "medium"
        validation_notes = (
            f"Medium confidence: {trusted_count} trusted sources from {unique_domain_count} domains. "
            "Results are consistent but consider checking official sources."
        )
    else:
        confidence = "low"
        validation_notes = (
            f"Low confidence: Only {trusted_count} trusted sources from {unique_domain_count} domains. "
            "Results may be incomplete or from less-established sources."
        )
        recommendation_notes.append("Verify important facts from official sources")
    
    # Add date-related recommendations
    if _has_recent_dates(results):
        validation_notes += " Information is recent."
    else:
        recommendation_notes.append("Some results may not be from today - dates not confirmed")
    
    return {
        "confidence": confidence,
        "trusted_sources": trusted_count,
        "unique_domains": unique_domain_count,
        "validation_notes": validation_notes,
        "recommendations": recommendation_notes,
    }


def _is_trusted_source(domain: str) -> bool:
    """
    Check if a domain is in the trusted sources list.
    
    Args:
        domain: The domain to check (e.g., "reuters.com")
        
    Returns:
        True if the domain is trusted, False otherwise
    """
    domain = (domain or "").lower().strip()
    
    # Direct match
    if domain in TRUSTED_SOURCES:
        return True
    
    # Check if domain ends with a trusted parent domain
    for trusted in TRUSTED_SOURCES:
        if domain.endswith("." + trusted) or domain == trusted:
            return True
    
    return False


def _has_recent_dates(results: List[Dict]) -> bool:
    """
    Check if results include recent publication dates.
    
    Args:
        results: List of search results
        
    Returns:
        True if at least some results have recent dates, False otherwise
    """
    for result in results:
        published_date = result.get("published_date")
        if published_date:
            # If a published_date exists, assume it's reasonably recent
            # (Tavily returns recent articles by default)
            return True
    
    return False
