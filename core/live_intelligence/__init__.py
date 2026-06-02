"""
Live Intelligence Module

Provides real-time information retrieval using web search and news sources.
Detects when user queries require current/live information and enriches responses
with up-to-date context from trusted sources.
"""

from .realtime_detector import requires_realtime
from .web_search import search_live_web
from .news_engine import get_live_news_context
from .source_validator import validate_sources
from .live_response_builder import build_live_prompt

__all__ = [
    "requires_realtime",
    "search_live_web",
    "get_live_news_context",
    "validate_sources",
    "build_live_prompt",
]
