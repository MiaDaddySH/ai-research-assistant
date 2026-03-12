from __future__ import annotations

from fastapi import FastAPI

from app.agent import run_research
from app.schemas import ResearchRequest, ResearchResponse

app = FastAPI(title="AI Research Assistant")


# 基本的健康检查端点，确认后端服务正在运行
@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "AI Research Assistant backend is running"}


# 主要的研究端点，接受用户提问并返回研究结果
@app.post("/research", response_model=ResearchResponse)
async def research(req: ResearchRequest) -> ResearchResponse:
    return await run_research(req.question)
