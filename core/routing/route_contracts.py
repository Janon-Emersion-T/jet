from dataclasses import dataclass, field
from typing import Callable, List, Optional, Dict, Any


@dataclass
class RouteModule:
    name: str
    domain: str
    handler: Callable
    description: str
    examples: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    intents: List[str] = field(default_factory=list)
    canonical_commands: List[str] = field(default_factory=list)
    safety_level: str = "normal"
    requires_intent_arg: bool = False


@dataclass
class RouteDecision:
    module: Optional[RouteModule]
    confidence: float
    reason: str
    canonical_text: str
    scores: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
