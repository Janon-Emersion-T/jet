import os
import re
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

from core.nlp.phase000a_foundation_router import INTENT_EXAMPLES

# JARVIS NLP is designed to operate against locally cached models only.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

try:
    import spacy
except Exception:
    spacy = None

try:
    from sentence_transformers import SentenceTransformer, CrossEncoder, util
except Exception:
    SentenceTransformer = None
    CrossEncoder = None
    util = None


_SPACY_MODEL = None
_EMBEDDING_MODEL = None
_CROSS_ENCODER = None
_INTENT_PHRASES = []
_INTENT_LABELS = []
_INTENT_EMBEDDINGS = None


MODEL_PRIORITY = [
    os.getenv("JARVIS_EMBEDDING_MODEL", "").strip(),
    "BAAI/bge-small-en-v1.5",
    "sentence-transformers/all-mpnet-base-v2",
    "sentence-transformers/all-MiniLM-L6-v2",
]


CROSS_ENCODER_PRIORITY = [
    os.getenv("JARVIS_RERANKER_MODEL", "").strip(),
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
]


def _valid_models(models: List[str]) -> List[str]:
    return [m for m in models if m]


def get_spacy_model():
    global _SPACY_MODEL

    if _SPACY_MODEL is not None:
        return _SPACY_MODEL

    if spacy is None:
        return None

    for model_name in ["en_core_web_trf", "en_core_web_sm"]:
        try:
            _SPACY_MODEL = spacy.load(model_name)
            return _SPACY_MODEL
        except Exception:
            continue

    return None


def get_embedding_model():
    global _EMBEDDING_MODEL

    if _EMBEDDING_MODEL is not None:
        return _EMBEDDING_MODEL

    if SentenceTransformer is None:
        return None

    for model_name in _valid_models(MODEL_PRIORITY):
        try:
            _EMBEDDING_MODEL = SentenceTransformer(
                model_name,
                local_files_only=True,
            )
            return _EMBEDDING_MODEL
        except Exception:
            continue

    return None


def get_cross_encoder():
    global _CROSS_ENCODER

    if _CROSS_ENCODER is not None:
        return _CROSS_ENCODER

    if CrossEncoder is None:
        return None

    for model_name in _valid_models(CROSS_ENCODER_PRIORITY):
        try:
            _CROSS_ENCODER = CrossEncoder(
                model_name,
                local_files_only=True,
            )
            return _CROSS_ENCODER
        except Exception:
            continue

    return None


def _prepare_intent_phrases():
    phrases = []
    labels = []

    for intent, examples in INTENT_EXAMPLES.items():
        for example in examples:
            phrases.append(example)
            labels.append(intent)

    return phrases, labels


def _ensure_intent_embeddings():
    global _INTENT_PHRASES, _INTENT_LABELS, _INTENT_EMBEDDINGS

    model = get_embedding_model()
    if model is None:
        return None, None, None

    if _INTENT_EMBEDDINGS is not None:
        return _INTENT_PHRASES, _INTENT_LABELS, _INTENT_EMBEDDINGS

    _INTENT_PHRASES, _INTENT_LABELS = _prepare_intent_phrases()
    _INTENT_EMBEDDINGS = model.encode(
        _INTENT_PHRASES,
        convert_to_tensor=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return _INTENT_PHRASES, _INTENT_LABELS, _INTENT_EMBEDDINGS


def semantic_tokenize(text: str):
    nlp = get_spacy_model()

    if not nlp:
        return None

    doc = nlp(text)

    return [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and token.text.strip()
    ]


def semantic_entities(text: str) -> Dict[str, str]:
    entities = {}
    nlp = get_spacy_model()

    if not nlp:
        return entities

    doc = nlp(text)

    for ent in doc.ents:
        key = f"entity_{ent.label_.lower()}"
        if key not in entities:
            entities[key] = ent.text

    quoted = re.findall(r'"([^"]+)"|\'([^\']+)\'', text)
    quoted_values = [a or b for a, b in quoted if a or b]
    if quoted_values:
        entities["quoted_text"] = quoted_values[0]

    return entities


def classify_with_embeddings(text: str) -> Tuple[str, float, Optional[str]]:
    model = get_embedding_model()
    phrases, labels, embeddings = _ensure_intent_embeddings()

    if model is None or util is None or embeddings is None:
        return "general", 0.0, None

    try:
        input_embedding = model.encode(
            text,
            convert_to_tensor=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        scores = util.cos_sim(input_embedding, embeddings)[0]
        top_k = min(5, len(phrases))
        top_results = scores.topk(k=top_k)

        candidates = []
        for score, idx in zip(top_results.values, top_results.indices):
            idx = int(idx)
            candidates.append(
                {
                    "intent": labels[idx],
                    "phrase": phrases[idx],
                    "score": float(score),
                }
            )

        best = candidates[0]

        reranker = get_cross_encoder()
        if reranker is not None and len(candidates) > 1:
            pairs = [[text, c["phrase"]] for c in candidates]
            rerank_scores = reranker.predict(pairs)

            best_index = max(range(len(candidates)), key=lambda i: float(rerank_scores[i]))
            best = candidates[best_index]

            # blend bi-encoder confidence with cross-encoder signal
            raw_rerank = float(rerank_scores[best_index])
            rerank_confidence = 1.0 / (1.0 + pow(2.71828, -raw_rerank))
            best["score"] = max(best["score"], rerank_confidence)

        if best["score"] < 0.43:
            return "general", best["score"], best["phrase"]

        return best["intent"], best["score"], best["phrase"]

    except Exception:
        return "general", 0.0, None
