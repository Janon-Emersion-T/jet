from typing import Optional, Tuple

from core.nlp.phase000a_foundation_router import INTENT_EXAMPLES


try:
    import spacy
except Exception:
    spacy = None

try:
    from sentence_transformers import SentenceTransformer, util
except Exception:
    SentenceTransformer = None
    util = None


_SPACY_MODEL = None
_EMBEDDING_MODEL = None


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

    try:
        _EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        return _EMBEDDING_MODEL
    except Exception:
        return None


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


def semantic_entities(text: str):
    entities = {}
    nlp = get_spacy_model()

    if not nlp:
        return entities

    doc = nlp(text)

    for ent in doc.ents:
        entities[f"entity_{ent.label_.lower()}"] = ent.text

    return entities


def classify_with_embeddings(text: str) -> Tuple[str, float, Optional[str]]:
    model = get_embedding_model()

    if model is None or util is None:
        return "general", 0.0, None

    try:
        input_embedding = model.encode(text, convert_to_tensor=True)

        best_intent = "general"
        best_score = 0.0
        best_phrase = None

        for intent, examples in INTENT_EXAMPLES.items():
            example_embeddings = model.encode(examples, convert_to_tensor=True)
            scores = util.cos_sim(input_embedding, example_embeddings)[0]

            max_score = float(scores.max())
            best_index = int(scores.argmax())

            if max_score > best_score:
                best_intent = intent
                best_score = max_score
                best_phrase = examples[best_index]

        if best_score < 0.40:
            return "general", best_score, best_phrase

        return best_intent, best_score, best_phrase

    except Exception:
        return "general", 0.0, None
