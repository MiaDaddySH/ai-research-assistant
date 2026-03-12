from __future__ import annotations

import asyncio

from app.schemas import ArticleItem, ResearchResponse, SourceItem
from app.services.openai_client import summarize_article
from app.tools.fetch import fetch_article_content
from app.tools.search import search_web


async def process_article(question: str, item: dict[str, str]) -> ArticleItem:
    title = item.get("title", "")
    url = item.get("url", "")
    snippet = item.get("content", "")

    article_content = await fetch_article_content(url)

    if article_content.startswith("Failed") or article_content.startswith("No article"):
        article_summary = "Unable to generate summary because article content could not be extracted."
    else:
        try:
            article_summary = await summarize_article(question, article_content)
        except Exception as exc:
            article_summary = f"Failed to summarize article: {exc}"

    return ArticleItem(
        title=title,
        url=url,
        snippet=snippet,
        article_content=article_content,
        article_summary=article_summary,
    )


async def run_research(question: str) -> ResearchResponse:
    search_results = await search_web(question)

    tasks = [process_article(question, item) for item in search_results]
    articles = await asyncio.gather(*tasks)

    sources = [SourceItem(title=article.title, url=article.url) for article in articles]

    key_points = [article.title for article in articles if article.title][:3]

    return ResearchResponse(
        question=question,
        summary="Article-level summaries generated successfully. Final synthesis will be added in Step 4B.",
        key_points=key_points,
        sources=sources,
        articles=articles,
    )