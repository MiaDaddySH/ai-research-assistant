from tavily import TavilyClient
from app.config import get_settings

settings = get_settings()

client = TavilyClient(api_key=settings.tavily_api_key)

async def search_web(query: str, max_results: int = 5) -> list[dict]:
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
    )

    results = response.get("results", [])

    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
        }
        for item in results
    ]