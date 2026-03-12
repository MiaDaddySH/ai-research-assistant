from __future__ import annotations

from pydantic import BaseModel, Field


# 代表研究请求的输入模型，包含用户提问
class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)


# 代表每个信息来源的基本信息，包括标题和URL等
class SourceItem(BaseModel):
    title: str
    url: str


# 代表每个搜索结果的详细信息，包括标题、URL、内容摘要、全文内容和文章总结等
class ArticleItem(BaseModel):
    title: str
    url: str
    snippet: str
    article_content: str
    article_summary: str | None = None


# 代表研究结果的输出模型，包含用户提问、综合总结、关键要点、信息来源列表和文章详情列表等
class ResearchResponse(BaseModel):
    question: str
    summary: str
    key_points: list[str]
    sources: list[SourceItem]
    articles: list[ArticleItem]
