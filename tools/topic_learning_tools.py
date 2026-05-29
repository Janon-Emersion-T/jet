import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse, parse_qs, unquote

from core.vector_memory.vector_store import add_vector_memory


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _chunk_text(text: str, max_chars: int = 1200):
    words, chunks, current = text.split(), [], []

    for word in words:
        current.append(word)
        if len(" ".join(current)) >= max_chars:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


def _source_score(url: str, title: str, topic: str) -> int:
    domain = urlparse(url).netloc.lower()
    score = 3

    trusted = [
        ".gov", ".edu", ".ac.", "wikipedia.org", "britannica.com",
        "worldbank.org", "imf.org", "un.org", "who.int", "unesco.org",
        "cia.gov", "gov.lk", "cbsl.gov.lk", "statistics.gov.lk"
    ]

    for item in trusted:
        if item in domain:
            score += 3

    for word in topic.lower().split():
        if word in f"{title} {url}".lower():
            score += 1

    return max(1, min(score, 10))


def _wikipedia_sources(topic: str):
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "opensearch",
        "search": topic,
        "limit": 5,
        "namespace": 0,
        "format": "json",
    }

    headers = {"User-Agent": "JARVIS-Learning-Engine/1.0"}

    response = requests.get(url, params=params, headers=headers, timeout=20)
    response.raise_for_status()

    data = response.json()
    titles = data[1]
    links = data[3]

    results = []

    for title, link in zip(titles, links):
        results.append({
            "title": title,
            "url": link,
            "score": _source_score(link, title, topic),
        })

    return results


def _duckduckgo_sources(topic: str):
    search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(topic)}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for link in soup.select("a.result__a"):
        href = link.get("href")
        title = _clean_text(link.get_text(" "))

        if not href:
            continue

        if "uddg=" in href:
            parsed = urlparse(href)
            qs = parse_qs(parsed.query)
            href = unquote(qs.get("uddg", [""])[0])

        if not href.startswith("http"):
            continue

        results.append({
            "title": title,
            "url": href,
            "score": _source_score(href, title, topic),
        })

    return results


def _search_web(topic: str, max_results: int = 8):
    results = []

    try:
        results.extend(_wikipedia_sources(topic))
    except Exception:
        pass

    try:
        results.extend(_duckduckgo_sources(topic))
    except Exception:
        pass

    seen = set()
    unique = []

    for item in results:
        if item["url"] in seen:
            continue

        seen.add(item["url"])
        unique.append(item)

    unique = sorted(unique, key=lambda x: x["score"], reverse=True)
    return unique[:max_results]


def _extract_page_text(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=20)

    if response.status_code != 200:
        return None, f"HTTP {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "iframe", "nav", "footer"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"
    text = _clean_text(soup.get_text(" "))

    if len(text) < 300:
        return None, "Not enough readable content"

    return {"title": title, "text": text}, None


def learn_topic(topic: str, max_sources: int = 5, delay: float = 1.5) -> str:
    topic = topic.strip()

    if not topic:
        return "Topic is required. Example: learn about Sri Lanka"

    search_results = _search_web(topic, max_results=10)

    if not search_results:
        return f"No useful sources found for: {topic}"

    learned_sources = 0
    learned_chunks = 0
    skipped = []

    for source in search_results:
        if learned_sources >= max_sources:
            break

        url = source["url"]

        try:
            page, error = _extract_page_text(url)

            if error:
                skipped.append(f"{url} — {error}")
                continue

            chunks = _chunk_text(page["text"])

            for index, chunk in enumerate(chunks[:8]):
                memory_text = (
                    f"Dynamic topic learning\n"
                    f"Topic: {topic}\n"
                    f"Source URL: {url}\n"
                    f"Source title: {page['title']}\n"
                    f"Trust score: {source['score']}/10\n"
                    f"Chunk: {index + 1}\n\n"
                    f"{chunk}"
                )

                add_vector_memory(
                    memory_text,
                    tags=["dynamic-learning", "topic-learning", topic.lower()],
                    source="online-research",
                    importance=source["score"],
                )

                learned_chunks += 1

            learned_sources += 1
            time.sleep(delay)

        except Exception as e:
            skipped.append(f"{url} — {e}")

    lines = [
        "DYNAMIC TOPIC LEARNING COMPLETE",
        f"Topic: {topic}",
        f"Sources learned: {learned_sources}",
        f"Memory chunks saved: {learned_chunks}",
        "",
        "Discovered sources:",
    ]

    for item in search_results[:5]:
        lines.append(f"- {item['title']} | score {item['score']}/10 | {item['url']}")

    if skipped:
        lines.append("")
        lines.append("Skipped:")
        lines.extend(skipped[:5])

    return "\n".join(lines)