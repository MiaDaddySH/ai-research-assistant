from __future__ import annotations

import asyncio
from typing import Any

from tavily import TavilyClient

from app.config import get_settings

settings = get_settings()
client = TavilyClient(api_key=settings.tavily_api_key)


# 定义一个同步函数，使用Tavily API进行网页搜索，返回搜索结果列表
def _search_web_sync(query: str, max_results: int) -> list[dict[str, str]]:
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


# 定义一个异步函数，包装同步搜索函数，使用asyncio.to_thread在后台线程中执行同步代码
async def search_web(query: str, max_results: int | None = None) -> list[dict[str, str]]:
    final_max_results = max_results or settings.research_max_results
    return await asyncio.to_thread(_search_web_sync, query, final_max_results)
