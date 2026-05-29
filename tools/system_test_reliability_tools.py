from __future__ import annotations

import json
from pathlib import Path


SYSTEM_TEST_RELIABILITY_DIR = Path("storage/system_test_reliability")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(SYSTEM_TEST_RELIABILITY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def webhook_retry_tester() -> str:
    return _render("WEBHOOK RETRY TESTER - PHASE 1661", "webhook-retry overview", "webhook_retry_tester.json", "retry_paths", "durable", "dropping", "Retry paths tracked", "Durable paths", "Dropping paths", "Guardrail: retry testing should preserve idempotency awareness and avoid conflating transient network issues with permanent handler bugs.")


def queue_worker_tester() -> str:
    return _render("QUEUE WORKER TESTER - PHASE 1662", "queue-worker overview", "queue_worker_tester.json", "worker_checks", "healthy", "failing", "Worker checks tracked", "Healthy checks", "Failing checks", "Guardrail: queue-worker testing should preserve queue backend context and distinguish poison jobs from worker instability.")


def permission_boundary_tester() -> str:
    return _render("PERMISSION BOUNDARY TESTER - PHASE 1663", "permission-boundary overview", "permission_boundary_tester.json", "boundary_checks", "enforced", "leaky", "Boundary checks tracked", "Enforced checks", "Leaky checks", "Guardrail: permission boundary testing should preserve least-privilege framing and require reproducible evidence before labeling an access leak.")


def multi_tenant_leak_tester() -> str:
    return _render("MULTI-TENANT LEAK TESTER - PHASE 1664", "multi-tenant-leak overview", "multi_tenant_leak_tester.json", "tenant_checks", "isolated", "leaking", "Tenant checks tracked", "Isolated checks", "Leaking checks", "Guardrail: tenant-leak testing should preserve data privacy and never expose real tenant content in reports.")


def database_integrity_tester() -> str:
    return _render("DATABASE INTEGRITY TESTER - PHASE 1665", "database-integrity overview", "database_integrity_tester.json", "integrity_checks", "passing", "corrupted", "Integrity checks tracked", "Passing checks", "Corrupted checks", "Guardrail: integrity testing should preserve transactional context and avoid presenting partial validation as a full data-health guarantee.")


def performance_baseline_tester() -> str:
    return _render("PERFORMANCE BASELINE TESTER - PHASE 1666", "performance-baseline overview", "performance_baseline_tester.json", "baseline_runs", "stable", "regressed", "Baseline runs tracked", "Stable runs", "Regressed runs", "Guardrail: performance baselines should preserve environment parity and note when noise may exceed the detected difference.")


def load_test_planner() -> str:
    return _render("LOAD-TEST PLANNER - PHASE 1667", "load-test-planning overview", "load_test_planner.json", "load_profiles", "realistic", "unsafe", "Load profiles tracked", "Realistic profiles", "Unsafe profiles", "Guardrail: load-test planning should preserve production safety, rate-limit awareness, and explicit approval before high-impact runs.")


def slow_query_monitor() -> str:
    return _render("SLOW-QUERY MONITOR - PHASE 1668", "slow-query overview", "slow_query_monitor.json", "query_profiles", "acceptable", "slow", "Query profiles tracked", "Acceptable profiles", "Slow profiles", "Guardrail: slow-query analysis should preserve workload context, index-history nuance, and avoid suggesting destructive changes without evidence.")


def memory_leak_detector() -> str:
    return _render("MEMORY LEAK DETECTOR - PHASE 1669", "memory-leak overview", "memory_leak_detector.json", "memory_profiles", "stable", "leaking", "Memory profiles tracked", "Stable profiles", "Leaking profiles", "Guardrail: leak detection should preserve sampling caveats and distinguish sustained growth from expected caching or warmup effects.")


def frontend_bundle_regression_watcher() -> str:
    return _render("FRONTEND BUNDLE REGRESSION WATCHER - PHASE 1670", "frontend-bundle overview", "frontend_bundle_regression.json", "bundle_checks", "contained", "bloated", "Bundle checks tracked", "Contained bundles", "Bloated bundles", "Guardrail: bundle regression analysis should preserve build-mode context and clearly separate feature-driven growth from accidental bloat.")
