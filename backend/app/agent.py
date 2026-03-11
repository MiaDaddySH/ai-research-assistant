from app.tools.search import search_web
from app.tools.fetch import fetch_article_content


async def run_research(question: str) -> dict:
    search_results = await search_web(question, max_results=3)

    enriched_articles = []

    for item in search_results:
        article_content = await fetch_article_content(item["url"])

        enriched_articles.append(
            {
                "title": item["title"],
                "url": item["url"],
                "snippet": item.get("content", ""),
                "article_content": article_content,
            }
        )

    sources = [
        {
            "title": article["title"],
            "url": article["url"],
        }
        for article in enriched_articles
    ]

    key_points = [
        article["title"] for article in enriched_articles[:3]
    ]

    summary = "Fetched article contents successfully. Summarization will be added in the next step."

    return {
        "question": question,
        "summary": summary,
        "key_points": key_points,
        "sources": sources,
        "articles": enriched_articles,
    }