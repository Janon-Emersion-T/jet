"""
News and Real-time Intelligence Engine

Orchestrates web search, source validation, and context gathering
for real-time information retrieval.
"""

from typing import Dict, List, Optional
from .web_search import search_live_web
from .source_validator import validate_sources


def get_live_news_context(query: str) -> Dict:
    """
    Retrieve live news and web intelligence context for a query.
    
    Args:
        query: The search query
        
    Returns:
        {
            "query": str,
            "results": List[Dict],
            "confidence": "low" | "medium" | "high",
            "sources_count": int,
            "validation": Dict,
            "summary_context": str
        }
    """
    
    # Perform web search
    results = search_live_web(query, max_results=5)
    
    # Check for errors
    error_result = _extract_error(results)
    if error_result:
        return {
            "query": query,
            "results": [],
            "confidence": "low",
            "sources_count": 0,
            "validation": {
                "confidence": "low",
                "trusted_sources": 0,
                "unique_domains": 0,
                "validation_notes": error_result,
                "recommendations": [],
            },
            "summary_context": error_result,
        }
    
    # Validate sources
    validation = validate_sources(results)
    
    # Extract sources count
    sources_count = validation.get("unique_domains", 0)
    
    # Build summary context
    summary_context = _build_summary_context(query, results, validation)
    
    return {
        "query": query,
        "results": results,
        "confidence": validation.get("confidence", "low"),
        "sources_count": sources_count,
        "validation": validation,
        "summary_context": summary_context,
    }


def _extract_error(results: List[Dict]) -> Optional[str]:
    """
    Extract error message if present in results.
    
    Args:
        results: Search results list
        
    Returns:
        Error message if found, None otherwise
    """
    if not results:
        return None
    
    for result in results:
        if result.get("type") == "error":
            return result.get("message", "Search error occurred")
    
    return None


def _build_summary_context(
    query: str,
    results: List[Dict],
    validation: Dict
) -> str:
    """
    Build a human-readable summary of the search context.
    
    Args:
        query: The original search query
        results: List of search results
        validation: Validation results
        
    Returns:
        A formatted string summarizing the search context
    """
    
    lines = [
        f"Query: {query}",
        f"Sources found: {validation.get('unique_domains', 0)}",
        f"Confidence: {validation.get('confidence', 'unknown').upper()}",
    ]
    
    # Add AI answer if available
    for result in results:
        if result.get("type") == "answer":
            lines.append(f"\nSummary: {result.get('content', '')}")
            break
    
    # Add top sources
    non_error_results = [r for r in results if r.get("type") != "error"]
    if non_error_results:
        lines.append("\nTop sources:")
        for i, result in enumerate(non_error_results[:3], 1):
            title = result.get("title", "")
            source = result.get("source", "")
            if title and source:
                lines.append(f"  {i}. {title} ({source})")
            elif source:
                lines.append(f"  {i}. {source}")
    
    # Add validation notes
    validation_notes = validation.get("validation_notes", "")
    if validation_notes:
        lines.append(f"\nValidation: {validation_notes}")
    
    # Add recommendations if confidence is low
    recommendations = validation.get("recommendations", [])
    if recommendations:
        lines.append("\nRecommendations:")
        for rec in recommendations:
            lines.append(f"  - {rec}")
    
    return "\n".join(lines)
