import re
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

from core.vector_memory.vector_store import add_vector_memory


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _chunk_text(text: str, max_chars: int = 1200):
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(" ".join(current)) >= max_chars:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks


def _same_domain(url: str, base_domain: str) -> bool:
    return urlparse(url).netloc == base_domain


def learn_website(start_url: str, max_pages: int = 50, delay: float = 1.0) -> str:
    parsed = urlparse(start_url)

    if not parsed.scheme.startswith("http"):
        return "Invalid URL. Use a full URL like https://www.gov.lk/"

    base_domain = parsed.netloc
    visited = set()
    queue = deque([start_url])
    learned_chunks = 0
    crawled_pages = 0
    errors = []

    headers = {
        "User-Agent": "JARVIS-Learning-Engine/1.0"
    }

    while queue and crawled_pages < max_pages:
        url = queue.popleft()

        if url in visited:
            continue

        visited.add(url)

        try:
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code != 200:
                errors.append(f"{url} returned {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
                tag.decompose()

            title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled Page"
            page_text = _clean_text(soup.get_text(" "))

            if len(page_text) > 200:
                chunks = _chunk_text(page_text)

                for index, chunk in enumerate(chunks):
                    memory_text = (
                        f"Website learned content\n"
                        f"Source: {url}\n"
                        f"Title: {title}\n"
                        f"Chunk: {index + 1}/{len(chunks)}\n\n"
                        f"{chunk}"
                    )

                    add_vector_memory(
                        memory_text,
                        tags=["website-learning", base_domain],
                        source="website",
                        importance=6
                    )

                    learned_chunks += 1

            crawled_pages += 1

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"]).split("#")[0].rstrip("/")

                if not next_url.startswith("http"):
                    continue

                if _same_domain(next_url, base_domain) and next_url not in visited:
                    queue.append(next_url)

            time.sleep(delay)

        except Exception as e:
            errors.append(f"{url}: {e}")

    result = [
        "WEBSITE LEARNING COMPLETE",
        f"Start URL: {start_url}",
        f"Pages crawled: {crawled_pages}",
        f"Memory chunks saved: {learned_chunks}",
        f"Domain locked to: {base_domain}",
    ]

    if errors:
        result.append("\nErrors:")
        result.extend(errors[:10])

    return "\n".join(result)
