from __future__ import annotations

import asyncio

from app.schemas import ArticleItem, ResearchResponse, SourceItem
from app.services.openai_client import summarize_article, synthesize_research
from app.tools.fetch import fetch_article_content
from app.tools.search import search_web


def _is_valid_article_summary(summary: str | None) -> bool:
    if summary is None:
        return False

    invalid_prefixes = (
        "Failed",
        "Unable",
        "No summary returned",
        "Article content is empty",
    )

    return bool(summary.strip()) and not summary.startswith(invalid_prefixes)


async def process_article(question: str, item: dict[str, str]) -> ArticleItem:
    title = item.get("title", "")
    url = item.get("url", "")
    snippet = item.get("content", "")

    article_content = await fetch_article_content(url)

    if article_content.startswith("Failed") or article_content.startswith("No article"):
        article_summary = (
            "Unable to generate summary because article content could not be extracted."
        )
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

    article_summaries: list[str] = [
        summary
        for article in articles
        if (summary := article.article_summary) is not None and _is_valid_article_summary(summary)
    ]

    final_summary, final_key_points = await synthesize_research(
        question=question,
        article_summaries=article_summaries,
    )

    if not final_key_points:
        fallback_key_points = [article.title for article in articles if article.title]
        final_key_points = fallback_key_points[:3]

    return ResearchResponse(
        question=question,
        summary=final_summary,
        key_points=final_key_points,
        sources=sources,
        articles=articles,
    )
