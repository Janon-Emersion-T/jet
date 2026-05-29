from __future__ import annotations

import json
from pathlib import Path


QA_AUTOMATION_DIR = Path("storage/qa_automation")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(QA_AUTOMATION_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def autonomous_qa_test_designer() -> str:
    return _render("AUTONOMOUS QA TEST DESIGNER - PHASE 1651", "qa-test-design overview", "qa_test_designer.json", "test_plans", "covered", "missing", "Test plans tracked", "Covered plans", "Missing plans", "Guardrail: autonomous QA planning should preserve risk-based coverage, explicit assumptions, and human review for critical paths.")


def browser_regression_tester() -> str:
    return _render("BROWSER REGRESSION TESTER - PHASE 1652", "browser-regression overview", "browser_regression_tester.json", "browser_runs", "stable", "regressed", "Browser runs tracked", "Stable runs", "Regressed runs", "Guardrail: browser regression analysis should preserve environment parity and clearly distinguish flaky failures from likely regressions.")


def visual_ui_diff_engine() -> str:
    return _render("VISUAL UI DIFF ENGINE - PHASE 1653", "visual-ui-diff overview", "visual_ui_diff.json", "ui_diffs", "expected", "unexpected", "UI diffs tracked", "Expected diffs", "Unexpected diffs", "Guardrail: visual diffing should preserve viewport context, dynamic-content caveats, and avoid treating anti-aliasing noise as a product bug.")


def screenshot_based_bug_detector() -> str:
    return _render("SCREENSHOT-BASED BUG DETECTOR - PHASE 1654", "screenshot-bug overview", "screenshot_bug_detector.json", "bug_signals", "clean", "flagged", "Bug signals tracked", "Clean signals", "Flagged signals", "Guardrail: screenshot-based bug detection should preserve confidence visibility and avoid definitive claims without reproducible evidence.")


def accessibility_regression_checker() -> str:
    return _render("ACCESSIBILITY REGRESSION CHECKER - PHASE 1655", "accessibility-regression overview", "accessibility_regression.json", "a11y_checks", "passing", "failing", "Accessibility checks tracked", "Passing checks", "Failing checks", "Guardrail: accessibility analysis should preserve standards context, assistive-tech nuance, and explicit issue severity rather than generic scores.")


def mobile_viewport_auditor() -> str:
    return _render("MOBILE VIEWPORT AUDITOR - PHASE 1656", "mobile-viewport overview", "mobile_viewport_auditor.json", "viewport_checks", "responsive", "broken", "Viewport checks tracked", "Responsive checks", "Broken checks", "Guardrail: viewport auditing should preserve device-specific nuance and avoid assuming one breakpoint represents all mobile contexts.")


def form_validation_tester() -> str:
    return _render("FORM VALIDATION TESTER - PHASE 1657", "form-validation overview", "form_validation_tester.json", "form_paths", "validated", "unsafe", "Form paths tracked", "Validated paths", "Unsafe paths", "Guardrail: validation testing should preserve server/client distinction and avoid assuming UI-only checks guarantee backend safety.")


def auth_flow_tester() -> str:
    return _render("AUTH-FLOW TESTER - PHASE 1658", "auth-flow overview", "auth_flow_tester.json", "auth_paths", "passing", "broken", "Auth paths tracked", "Passing paths", "Broken paths", "Guardrail: auth-flow testing should preserve credential safety, session isolation, and explicit handling of multi-factor or environment-specific flows.")


def payment_flow_sandbox_tester() -> str:
    return _render("PAYMENT-FLOW SANDBOX TESTER - PHASE 1659", "payment-flow overview", "payment_flow_sandbox.json", "payment_paths", "passing", "blocked", "Payment paths tracked", "Passing paths", "Blocked paths", "Guardrail: payment-flow testing should preserve sandbox-only boundaries and never imply production billing safety from isolated test runs.")


def api_contract_tester() -> str:
    return _render("API CONTRACT TESTER - PHASE 1660", "api-contract overview", "api_contract_tester.json", "contract_checks", "compatible", "breaking", "Contract checks tracked", "Compatible checks", "Breaking checks", "Guardrail: contract testing should preserve versioning context, optional-field nuance, and differentiate schema drift from tolerated changes.")
