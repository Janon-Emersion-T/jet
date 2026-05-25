from urllib.parse import urlparse


BLOCKED_HOSTS = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
}


def safe_url(url: str) -> str:
    url = (url or "").strip()

    if not url:
        raise ValueError("URL is required.")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if parsed.scheme not in ["http", "https"]:
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")

    if parsed.hostname in BLOCKED_HOSTS:
        raise ValueError("Blocked local/internal browser target.")

    return url


def normalize_domain(domain: str) -> str:
    domain = (domain or "").lower().strip()
    domain = domain.replace("https://", "").replace("http://", "")
    domain = domain.replace("www.", "")
    return domain.strip("/")
