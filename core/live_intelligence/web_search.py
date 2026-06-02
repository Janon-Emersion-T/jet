"""
Web Search Module

Provides live web search using Tavily API.
Handles API integration, error handling, and result normalization.
"""

import os
from typing import List, Dict, Optional
import json


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
    
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    
    if not api_key:
        return [
            {
                "type": "error",
                "message": "TAVILY_API_KEY environment variable not set. "
                          "Live web search is not configured."
            }
        ]
    
    try:
        from tavily import TavilyClient
    except ImportError:
        return [
            {
                "type": "error",
                "message": "Tavily Python package not installed. "
                          "Install with: pip install tavily-python"
            }
        ]
    
    try:
        client = TavilyClient(api_key=api_key)
        
        # Perform the search with news context
        response = client.search(
            query=query,
            max_results=max_results,
            include_answer=True,
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
        
        return normalized if normalized else [
            {
                "type": "error",
                "message": "No results found for the query."
            }
        ]
        
    except Exception as e:
        return [
            {
                "type": "error",
                "message": f"Web search failed: {str(e)}. "
                          "Please check your internet connection and API key."
            }
        ]


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
