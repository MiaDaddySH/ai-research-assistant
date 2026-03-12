from __future__ import annotations

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)


class SourceItem(BaseModel):
    title: str
    url: str


class ArticleItem(BaseModel):
    title: str
    url: str
    snippet: str
    article_content: str
    article_summary: str | None = None


class ResearchResponse(BaseModel):
    question: str
    summary: str
    key_points: list[str]
    sources: list[SourceItem]
    articles: list[ArticleItem]
