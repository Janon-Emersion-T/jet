"""
Real-time Intent Detector

Detects if a user query requires live, current, or real-time information
based on keywords and temporal references.
"""

import re
from typing import Set


# Keywords that indicate a query needs real-time/current information
REALTIME_KEYWORDS = {
    # Temporal indicators
    "current", "latest", "today", "now", "live", "breaking", 
    "right now", "at this moment", "this week", "this month",
    "recently", "just now", "just happened", "happening now",
    
    # News and information
    "news", "status", "update", "latest news", "breaking news",
    "recent", "currently", "ongoing", "active",
    
    # Financial/price indicators
    "price", "stock", "bitcoin", "crypto", "market", "trading",
    "cost", "rate", "usd", "dollar", "pound", "euro",
    
    # Weather and natural phenomena
    "weather", "temperature", "forecast", "climate", "wind",
    "rain", "snow", "forecast", "storm", "hurricane", "earthquake",
    
    # Geopolitical
    "war", "conflict", "peace talks", "negotiations", "agreement",
    "election", "voting", "protest", "demonstration", "strike",
    "incident", "disaster", "emergency", "outbreak",
    
    # Sports and events
    "score", "game", "match", "sports", "tournament", "championship",
    "standings", "season", "playoffs", "world cup",
    
    # Technology
    "launch", "release", "announcement", "product launch",
    "ai news", "technology news", "startup news",
    
    # Health and medicine
    "pandemic", "epidemic", "virus spread", "outbreak", "vaccine",
    "health alert", "disease update",
}


def requires_realtime(user_input: str) -> bool:
    """
    Determine if user input requires real-time/live information.
    
    Args:
        user_input: The user's question or command
        
    Returns:
        True if the query appears to need real-time information, False otherwise
    """
    if not user_input:
        return False
    
    # Normalize the input
    text = user_input.lower().strip()
    
    # Remove common punctuation but preserve structure
    text = re.sub(r'[?!,;:"\']', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into words for keyword matching
    words = text.split()
    
    # Check for explicit real-time keyword matches
    for keyword in REALTIME_KEYWORDS:
        # Allow both exact word match and substring match for multi-word keywords
        if ' ' in keyword:
            if keyword in text:
                return True
        else:
            if keyword in words:
                return True
    
    # Check for patterns that indicate current/real-time context
    # Examples: "is X happening", "what's happening", "did X just", "what will X do today"
    realtime_patterns = [
        r'\b(?:is|are|was|were)\s+(?:\w+\s+)?(?:happening|occurring|going|going on)\b',
        r'\bwhat(?:\'s)?\s+(?:happening|going on|the status)\b',
        r'\bdid\s+(?:\w+\s+)?just\b',
        r'\bwhat\s+(?:will|can)\s+\w+\s+(?:do|say|announce)\s+(?:today|this week|this month)\b',
        r'\bhow\s+(?:\w+\s+)?(?:is|are|was|were)\b.*\b(?:today|now|currently)\b',
        r'\bas\s+of\s+(?:today|now|this\s+week)\b',
        r'\brecent(?:ly)?\b',
        r'\bup\s*-*\s*to\s*-*\s*date\b',
        r'\btodayis\b',
    ]
    
    for pattern in realtime_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    # Check for questions about specific current events
    # Pattern: "what about [topic]" where topic suggests current events
    event_topics = [
        "middle east", "ukraine", "russia", "china", "covid", "election",
        "stock market", "crypto market", "tech industry", "ai news"
    ]
    
    for topic in event_topics:
        if topic in text and any(word in text for word in ["what", "how", "tell", "about", "status"]):
            return True
    
    return False
