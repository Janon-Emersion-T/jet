import importlib
from typing import Any

from core.nlp.production_config import load_nlp_config
from core.nlp.phase000_engine import NLPResult as Phase000NLPResult

ENGINE_MODULES = {
    "phase000": "core.nlp.phase000_engine",
}

SUPPORTED_ENGINES = list(ENGINE_MODULES.keys())

NLPResult = Phase000NLPResult


def _get_engine_name() -> str:
    config = load_nlp_config()
    return str(config.get("analysis_engine", "phase000")).lower().strip()


def _load_engine_module(engine_name: str) -> Any:
    module_path = ENGINE_MODULES.get(engine_name, ENGINE_MODULES["phase000"])
    try:
        return importlib.import_module(module_path)
    except ImportError:
        return importlib.import_module(ENGINE_MODULES["phase000"])


def _get_engine_module() -> Any:
    engine_name = _get_engine_name()
    return _load_engine_module(engine_name)


def analyze_command(user_input: str) -> NLPResult:
    engine = _get_engine_module()
    return engine.analyze_command(user_input)


def classify_intent_nlp(user_input: str) -> str:
    engine = _get_engine_module()
    return engine.classify_intent_nlp(user_input)


def format_nlp_report(user_input: str) -> str:
    engine = _get_engine_module()
    return engine.format_nlp_report(user_input)

