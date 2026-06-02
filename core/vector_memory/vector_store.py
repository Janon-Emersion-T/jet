from pathlib import Path
from datetime import datetime
import hashlib
import json

STORAGE_DIR = Path("storage/vector_memory")
META_FILE = STORAGE_DIR / "vector_memory.json"
CHROMA_DIR = STORAGE_DIR / "chroma"

DEFAULT_COLLECTION = "jarvis_memory"


def _ensure_storage():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)


def _load_meta():
    _ensure_storage()
    if not META_FILE.exists():
        return []
    try:
        return json.loads(META_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_meta(data):
    _ensure_storage()
    META_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def _memory_id(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:16]


def _score_importance(text: str, source: str = "manual") -> int:
    text_lower = text.lower()
    score = 3

    high_value_terms = [
        "prefer", "always", "never", "important", "password",
        "project", "client", "company", "architecture", "decision",
        "rule", "remember", "deadline"
    ]

    for term in high_value_terms:
        if term in text_lower:
            score += 1

    if source in ["preference", "project", "system"]:
        score += 2

    return max(1, min(score, 10))


def add_vector_memory(text: str, tags=None, source="manual", importance=None):
    _ensure_storage()

    text = text.strip()
    if not text:
        return "Memory text is required."

    tags = tags or []
    memory_id = _memory_id(text)
    meta = _load_meta()

    if any(item["id"] == memory_id for item in meta):
        return "Vector memory already exists."

    item = {
        "id": memory_id,
        "text": text,
        "tags": tags,
        "source": source,
        "importance": importance if importance is not None else _score_importance(text, source),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": None,
        "active": True,
    }

    meta.append(item)
    _save_meta(meta)

    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_or_create_collection(DEFAULT_COLLECTION)
        collection.add(
            ids=[memory_id],
            documents=[text],
            metadatas=[{
                "tags": ",".join(tags),
                "source": source,
                "importance": item["importance"],
                "created_at": item["created_at"],
                "active": True,
            }]
        )
    except Exception as e:
        return f"Metadata saved, but ChromaDB indexing failed: {e}"

    return f"Vector memory saved. ID: {memory_id}"


def search_vector_memory(query: str, limit: int = 5):
    _ensure_storage()

    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_or_create_collection(DEFAULT_COLLECTION)

        results = collection.query(
            query_texts=[query],
            n_results=limit,
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]

        if not docs:
            return "No semantic memory found."

        output = ["SEMANTIC MEMORY RESULTS"]
        for idx, doc in enumerate(docs):
            meta = metas[idx] if idx < len(metas) else {}
            memory_id = ids[idx] if idx < len(ids) else "unknown"
            output.append(
                f"\n- ID: {memory_id}\n"
                f"  Source: {meta.get('source', 'unknown')}\n"
                f"  Importance: {meta.get('importance', 'unknown')}\n"
                f"  Memory: {doc}"
            )

        return "\n".join(output)

    except Exception as e:
        return f"Semantic memory search failed: {e}"


def list_vector_memories(limit: int = 20):
    meta = [item for item in _load_meta() if item.get("active", True)]
    meta = sorted(meta, key=lambda x: x.get("importance", 0), reverse=True)

    if not meta:
        return "No vector memories saved yet."

    lines = ["VECTOR MEMORY INDEX"]
    for item in meta[:limit]:
        lines.append(
            f"- {item['id']} | importance {item['importance']} | "
            f"source {item['source']} | tags {', '.join(item.get('tags', []))}\n"
            f"  {item['text'][:160]}"
        )

    return "\n".join(lines)


def list_vector_memory_data(limit: int = 20):
    meta = [item for item in _load_meta() if item.get("active", True)]
    meta = sorted(
        meta,
        key=lambda item: (
            -int(item.get("importance", 0) or 0),
            item.get("created_at", ""),
        ),
    )
    return meta[:limit]


def get_vector_memory_summary():
    meta = _load_meta()
    active = [item for item in meta if item.get("active", True)]

    source_counts = {}
    tag_counts = {}

    for item in active:
        source = item.get("source", "unknown")
        source_counts[source] = source_counts.get(source, 0) + 1

        for tag in item.get("tags", []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    top_tags = sorted(
        tag_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )[:8]

    return {
        "total": len(meta),
        "active": len(active),
        "inactive": len(meta) - len(active),
        "source_counts": dict(sorted(source_counts.items(), key=lambda item: (-item[1], item[0]))),
        "top_tags": [
            {"tag": tag, "count": count}
            for tag, count in top_tags
        ],
    }


def cleanup_low_importance(threshold: int = 2):
    meta = _load_meta()
    changed = 0

    for item in meta:
        if item.get("importance", 0) <= threshold and item.get("active", True):
            item["active"] = False
            item["updated_at"] = datetime.now().isoformat(timespec="seconds")
            changed += 1

    _save_meta(meta)
    return f"Memory cleanup complete. Deactivated {changed} low-importance memories."
