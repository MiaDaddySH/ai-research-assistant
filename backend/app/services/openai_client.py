from __future__ import annotations

import json

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
    question: str,
    article_content: str,
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


def build_research_synthesis_messages(
    question: str,
    article_summaries: list[str],
) -> list[ChatCompletionMessageParam]:
    joined_summaries = "\n\n".join(
        f"Article {index + 1}:\n{summary}"
        for index, summary in enumerate(article_summaries)
        if summary.strip()
    )

    system_message: ChatCompletionSystemMessageParam = {
        "role": "system",
        "content": (
            "You are a careful research assistant. "
            "Based on multiple article summaries, generate a final research result for the user. "
            "Be concise, factual, and practical. "
            "Do not invent information. "
            "Return valid JSON only."
        ),
    }

    user_message: ChatCompletionUserMessageParam = {
        "role": "user",
        "content": f"""
User question:
{question}

Article summaries:
{joined_summaries}

Task:
Create a final research result based on the article summaries above.

Return JSON in this exact format:
{{
  "summary": "A concise final summary answering the user's question.",
  "key_points": [
    "Key point 1",
    "Key point 2",
    "Key point 3"
  ]
}}

Requirements:
- summary should be 4 to 6 sentences
- key_points should contain 3 to 5 items
- be factual and concise
- do not use markdown
- output valid JSON only
""".strip(),
    }

    return [system_message, user_message]


async def synthesize_research(
    question: str,
    article_summaries: list[str],
) -> tuple[str, list[str]]:
    valid_summaries = [summary for summary in article_summaries if summary.strip()]
    if not valid_summaries:
        return (
            "No valid article summaries were available to synthesize a final result.",
            [],
        )

    messages = build_research_synthesis_messages(question, valid_summaries)

    response = await client.chat.completions.create(
        model=settings.azure_openai_deployment,
        messages=messages,
        temperature=0.2,
        max_tokens=500,
    )

    content = response.choices[0].message.content
    if not content:
        return ("No final summary returned by the model.", [])

    try:
        parsed = json.loads(content)

        summary_raw = parsed.get("summary", "No summary returned.")
        key_points_raw = parsed.get("key_points", [])

        summary = summary_raw if isinstance(summary_raw, str) else "No summary returned."

        if isinstance(key_points_raw, list):
            key_points = [str(item).strip() for item in key_points_raw if str(item).strip()]
        else:
            key_points = []

        return summary, key_points[:5]
    except json.JSONDecodeError:
        return (content.strip(), [])
