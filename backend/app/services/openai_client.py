from __future__ import annotations

from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from app.config import get_settings

settings = get_settings()

client = AsyncOpenAI(
    api_key=settings.azure_openai_api_key,
    base_url=settings.azure_openai_base_url,
)


def build_article_summary_messages(
    question: str, article_content: str
) -> list[ChatCompletionMessageParam]:
    trimmed_content = article_content[: settings.summary_max_input_chars]

    system_message: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": (
            "You are a careful research assistant. "
            "Summarize the article in a concise and factual way based on the user's question. "
            "Focus only on relevant developments, facts, and insights. "
            "Do not invent information."
        ),
    }

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": f"""
User question:
{question}

Article content:
{trimmed_content}

Task:
Write a concise summary of this article that helps answer the user's question.

Requirements:
- Use 4 to 6 sentences.
- Focus on the most relevant information.
- Avoid bullet points.
- Avoid speculation.
""".strip(),
    }

    return [system_message, user_message]


async def summarize_article(question: str, article_content: str) -> str:
    if not article_content.strip():
        return "Article content is empty, so no summary could be generated."

    messages = build_article_summary_messages(question, article_content)

    response = await client.chat.completions.create(
        model=settings.azure_openai_deployment,
        messages=messages,
        temperature=0.2,
        max_tokens=300,
    )

    content = response.choices[0].message.content
    return content.strip() if content else "No summary returned by the model."