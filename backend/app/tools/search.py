from __future__ import annotations

import asyncio
import time
from typing import Any

from tavily import TavilyClient

from app.config import get_settings

settings = get_settings()
client = TavilyClient(api_key=settings.tavily_api_key)


def _search_web_sync(query: str, max_results: int) -> list[dict[str, str]]:
    last_error: Exception | None = None

    for attempt in range(3):
        try:
            response: dict[str, Any] = client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
            )

            results = response.get("results", [])

            normalized_results: list[dict[str, str]] = []
            for item in results:
                normalized_results.append(
                    {
                        "title": item.get("title", "") or "",
                        "url": item.get("url", "") or "",
                        "content": item.get("content", "") or "",
                    }
                )

            return normalized_results

        except Exception as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(1.0 * (attempt + 1))

    raise RuntimeError(f"Tavily search failed after retries: {last_error}") from last_error


async def search_web(query: str, max_results: int | None = None) -> list[dict[str, str]]:
    final_max_results = max_results or settings.research_max_results
    return await asyncio.to_thread(_search_web_sync, query, final_max_results)