from __future__ import annotations

import asyncio

from app.config import get_settings
from app.logger import setup_logger
from app.schemas import ArticleItem, ArticleProcessingItem, ResearchResponse, SourceItem
from app.services.openai_client import summarize_article, synthesize_research
from app.tools.fetch import fetch_article_content
from app.tools.search import search_web

settings = get_settings()
logger = setup_logger()


def _is_valid_article_summary(summary: str) -> bool:
    invalid_prefixes = (
        "Failed",
        "Unable",
        "No summary returned",
        "Article content is empty",
    )
    return bool(summary.strip()) and not summary.startswith(invalid_prefixes)


async def process_article(question: str, item: dict[str, str]) -> ArticleProcessingItem:
    title = item.get("title", "")
    url = item.get("url", "")
    snippet = item.get("content", "")

    logger.info("Processing article | title=%s | url=%s", title, url)

    fetch_result = await fetch_article_content(url)
    article_content = fetch_result.content

    if fetch_result.error:
        article_summary = (
            "Unable to generate summary because article content could not be extracted."
        )
        logger.warning(
            "Article extraction failed | title=%s | url=%s | error=%s",
            title,
            url,
            fetch_result.error,
        )
    else:
        try:
            article_summary = await summarize_article(question, article_content)
            logger.info("Article summary generated | title=%s", title)
        except Exception as exc:
            article_summary = f"Failed to summarize article: {exc}"
            logger.warning("Article summarization failed | title=%s | error=%s", title, exc)

    return ArticleProcessingItem(
        title=title,
        url=url,
        snippet=snippet,
        article_content=article_content,
        article_summary=article_summary,
    )


async def _process_article_with_limit(
    semaphore: asyncio.Semaphore,
    question: str,
    item: dict[str, str],
) -> ArticleProcessingItem:
    async with semaphore:
        return await process_article(question, item)


def _build_article_summaries(articles: list[ArticleProcessingItem]) -> list[str]:
    article_summaries: list[str] = []

    for article in articles:
        summary = article.article_summary
        if _is_valid_article_summary(summary):
            article_summaries.append(summary)

    return article_summaries


def _build_fallback_key_points(articles: list[ArticleProcessingItem]) -> list[str]:
    fallback_key_points = [article.title for article in articles if article.title]
    return fallback_key_points[:3]


async def run_research(question: str) -> ResearchResponse:
    logger.info("Research request received | question=%s", question)

    try:
        search_results = await search_web(question)
    except Exception as exc:
        logger.error("Research failed during web search | error=%s", exc)
        return ResearchResponse(
            question=question,
            summary=f"Research failed during web search: {exc}",
            key_points=[],
            sources=[],
            articles=[],
        )

    if not search_results:
        logger.info("No search results found")
        return ResearchResponse(
            question=question,
            summary="No search results were found for this question.",
            key_points=[],
            sources=[],
            articles=[],
        )

    semaphore = asyncio.Semaphore(settings.max_article_concurrency)

    tasks = [_process_article_with_limit(semaphore, question, item) for item in search_results]
    processed_articles = await asyncio.gather(*tasks)

    sources = [SourceItem(title=article.title, url=article.url) for article in processed_articles]
    article_summaries = _build_article_summaries(processed_articles)

    final_summary, final_key_points = await synthesize_research(
        question=question,
        article_summaries=article_summaries,
    )

    if not final_key_points:
        final_key_points = _build_fallback_key_points(processed_articles)

    articles = [
        ArticleItem(
            title=article.title,
            url=article.url,
            snippet=article.snippet,
            article_summary=article.article_summary,
        )
        for article in processed_articles
    ]

    logger.info(
        "Research completed | sources=%s | valid_summaries=%s | key_points=%s",
        len(sources),
        len(article_summaries),
        len(final_key_points),
    )

    return ResearchResponse(
        question=question,
        summary=final_summary,
        key_points=final_key_points,
        sources=sources,
        articles=articles,
    )
