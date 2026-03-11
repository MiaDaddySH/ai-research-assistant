import httpx
from bs4 import BeautifulSoup


async def fetch_article_content(url: str, max_chars: int = 8000) -> str:
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/122.0.0.0 Safari/537.36"
                    )
                },
            )
            response.raise_for_status()
    except Exception as e:
        return f"Failed to fetch article: {str(e)}"

    try:
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "header", "footer", "aside", "nav"]):
            tag.decompose()

        content_root = soup.find("article") or soup.find("main") or soup.body
        if not content_root:
            return "No article body found."

        text = content_root.get_text(separator="\n", strip=True)

        lines = [line.strip() for line in text.splitlines()]
        cleaned_lines = [line for line in lines if line]
        cleaned_text = "\n".join(cleaned_lines)

        return cleaned_text[:max_chars]

    except Exception as e:
        return f"Failed to parse article: {str(e)}"