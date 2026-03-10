from app.tools.search import search_web


async def run_research(question: str) -> dict:
    search_results = await search_web(question)

    sources = [
        {
            "title": item["title"],
            "url": item["url"],
        }
        for item in search_results
    ]

    key_points = [
        item["title"] for item in search_results[:3]
    ]

    summary = "This is a placeholder summary based on web search results."

    return {
        "question": question,
        "summary": summary,
        "key_points": key_points,
        "sources": sources,
    }