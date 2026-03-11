from pydantic import BaseModel
from typing import List


class ResearchRequest(BaseModel):
    question: str


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
    key_points: List[str]
    sources: List[SourceItem]
    articles: List[ArticleItem]