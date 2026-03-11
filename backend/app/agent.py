from app.tools.search import search_web
from app.tools.fetch import fetch_article_content
from app.services.openai_client import summarize_article


async def run_research(question: str) -> dict:
    search_results = await search_web(question, max_results=3)

    enriched_articles = []

    for item in search_results:
        article_content = await fetch_article_content(item["url"])

        if article_content.startswith("Failed") or article_content.startswith("No article"):
            article_summary = "Unable to generate summary because article content could not be extracted."
        else:
            try:
                article_summary = await summarize_article(question, article_content)
            except Exception as e:
                article_summary = f"Failed to summarize article: {str(e)}"

        enriched_articles.append(
            {
                "title": item["title"],
                "url": item["url"],
                "snippet": item.get("content", ""),
                "article_content": article_content,
                "article_summary": article_summary,
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

    return {
        "question": question,
        "summary": "Article-level summaries generated successfully. Final synthesis will be added in Step 4B.",
        "key_points": key_points,
        "sources": sources,
        "articles": enriched_articles,
    }