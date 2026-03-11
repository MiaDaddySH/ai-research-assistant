from openai import AsyncOpenAI
from app.config import get_settings

settings = get_settings()

client = AsyncOpenAI(
    api_key=settings.azure_openai_api_key,
    base_url=f"{settings.azure_openai_endpoint.rstrip('/')}/openai/v1/",
)

async def summarize_article(question: str, article_content: str) -> str:

    trimmed_content = article_content[:6000]

    system_prompt = (
        "You are a helpful research assistant. "
        "Summarize the article clearly and concisely based on the user's question."
    )

    user_prompt = f"""
User question:
{question}

Article content:
{trimmed_content}

Write a concise summary (4-6 sentences).
"""

    response = await client.chat.completions.create(
        model=settings.azure_openai_deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()