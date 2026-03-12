from __future__ import annotations

import httpx
from bs4 import BeautifulSoup

from app.config import get_settings

settings = get_settings()

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


def _clean_text(raw_text: str) -> str:
    lines = [line.strip() for line in raw_text.splitlines()]
    non_empty_lines = [line for line in lines if line]
    return "\n".join(non_empty_lines)


async def fetch_article_content(url: str, max_chars: int | None = None) -> str:
    final_max_chars = max_chars or settings.fetch_max_chars

    try:
        async with httpx.AsyncClient(
            timeout=settings.article_fetch_timeout_seconds,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
    except Exception as exc:
        return f"Failed to fetch article: {exc}"

    try:
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(
            ["script", "style", "noscript", "header", "footer", "aside", "nav", "form"]
        ):
            tag.decompose()

        content_root = soup.find("article") or soup.find("main") or soup.body
        if content_root is None:
            return "No article body found."

        raw_text = content_root.get_text(separator="\n", strip=True)
        cleaned_text = _clean_text(raw_text)

        if len(cleaned_text) < settings.article_min_length:
            return "No article body found."

        return cleaned_text[:final_max_chars]
    except Exception as exc:
        return f"Failed to parse article: {exc}"
