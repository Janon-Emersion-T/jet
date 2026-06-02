"""
Web Search Module

Provides live web search using Tavily API with a browser-backed fallback.
Handles API integration, error handling, and result normalization.
"""

import os
import re
from typing import List, Dict, Optional

from tools.browser_automation_tools import browser_google_results


def search_live_web(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search the web for live information using Tavily API.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        List of normalized search results with structure:
        {
            "title": str,
            "url": str,
            "content": str (snippet/summary),
            "published_date": str (optional),
            "source": str (domain)
        }
        
        If API is not available or no results, returns empty list or error dict.
    """
    
    safe_query = _sanitize_query(query)
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    
    if not api_key:
        fallback_results = _search_with_browser(safe_query, max_results=max_results)
        if fallback_results:
            return fallback_results
        return [
            {
                "type": "error",
                "message": "Live web search is not configured."
            }
        ]
    
    try:
        from tavily import TavilyClient
    except ImportError:
        fallback_results = _search_with_browser(safe_query, max_results=max_results)
        if fallback_results:
            return fallback_results
        return [
            {
                "type": "error",
                "message": "Live web search is unavailable because the Tavily Python package is not installed."
            }
        ]
    
    try:
        client = TavilyClient(api_key=api_key)

        # Keep the request conservative so live-news searches stay reliable.
        response = client.search(
            query=safe_query,
            max_results=max_results,
            include_answer="basic",
            search_depth="basic",
            topic="news",
        )
        
        # Normalize the results
        normalized = []
        
        # Extract the AI-generated answer if available
        if response.get("answer"):
            normalized.append(
                {
                    "type": "answer",
                    "content": response["answer"],
                    "source": "Tavily AI Summary"
                }
            )
        
        # Process each search result
        for result in response.get("results", []):
            normalized.append(
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "source": _extract_domain(result.get("url", "")),
                    "published_date": result.get("published_date", None),
                }
            )
        
        if normalized:
            return normalized

        fallback_results = _search_with_browser(safe_query, max_results=max_results)
        if fallback_results:
            return fallback_results

        return [
            {
                "type": "error",
                "message": "No live search results were found for the query."
            }
        ]

    except Exception:
        fallback_results = _search_with_browser(safe_query, max_results=max_results)
        if fallback_results:
            return fallback_results

        return [
            {
                "type": "error",
                "message": "Live web search is temporarily unavailable."
            }
        ]


def _sanitize_query(query: str) -> str:
    safe = " ".join((query or "").split())
    safe = re.sub(r"[\x00-\x1f\x7f]+", " ", safe).strip()
    return safe[:380]


def _search_with_browser(query: str, max_results: int = 5) -> List[Dict]:
    """
    Best-effort fallback search using the local browser automation parser.
    """
    if not query:
        return []

    try:
        raw = browser_google_results(query, limit=max_results)
    except Exception:
        return []

    if not raw or "RESULTS:" not in raw:
        return []

    results: List[Dict] = []
    current_title = ""
    current_url = ""

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if re.match(r"^\d+\.\s+", stripped):
            current_title = re.sub(r"^\d+\.\s+", "", stripped).strip()
            current_url = ""
            continue

        if stripped.startswith("http://") or stripped.startswith("https://"):
            current_url = stripped
            results.append(
                {
                    "title": current_title or stripped,
                    "url": current_url,
                    "content": current_title or stripped,
                    "source": _extract_domain(current_url),
                    "published_date": None,
                }
            )
            current_title = ""
            current_url = ""

    return results


def _extract_domain(url: str) -> str:
    """
    Extract domain name from URL.
    
    Args:
        url: The full URL
        
    Returns:
        The domain name (e.g., "reuters.com")
    """
    if not url:
        return "Unknown"
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        # Remove 'www.' prefix if present
        domain = domain.replace("www.", "")
        return domain or "Unknown"
    except Exception:
        return "Unknown"
