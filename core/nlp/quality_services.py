from dataclasses import dataclass
from typing import Callable, Dict, List


DEFAULT_CASES = [
    {"text": "git status", "intent": "devops"},
    {"text": "analyze project current", "intent": "project_analysis"},
    {"text": "search google for python", "intent": "google_search"},
    {"text": "read file main.py", "intent": "project_analysis"},
]


@dataclass
class AccuracyReport:
    total: int
    passed: int
    accuracy: float
    failures: List[Dict[str, str]]


def generate_test_suite() -> List[Dict[str, str]]:
    return list(DEFAULT_CASES)


def score_intents(classifier: Callable[[str], str],
                  cases: List[Dict[str, str]] | None = None) -> AccuracyReport:
    cases = cases or generate_test_suite()
    failures = []
    for case in cases:
        actual = classifier(case["text"])
        if actual != case["intent"]:
            failures.append({"text": case["text"], "expected": case["intent"], "actual": actual})
    passed = len(cases) - len(failures)
    return AccuracyReport(len(cases), passed, round(passed / len(cases), 3) if cases else 1.0, failures)


def analyze_failed_commands(report: AccuracyReport) -> List[str]:
    return [
        f"'{failure['text']}' resolved as {failure['actual']} instead of {failure['expected']}."
        for failure in report.failures
    ]


def suggest_registry_improvements(report: AccuracyReport) -> Dict[str, List[str]]:
    suggestions: Dict[str, List[str]] = {}
    for failure in report.failures:
        suggestions.setdefault(failure["expected"], []).append(failure["text"])
    return suggestions


def confidence_dashboard(confidence: float, safety_level: str, domain: str) -> Dict[str, object]:
    return {
        "confidence": confidence,
        "band": "high" if confidence >= 0.8 else "medium" if confidence >= 0.5 else "low",
        "safety_level": safety_level,
        "domain": domain,
    }
