from __future__ import annotations

from fastapi import FastAPI

from app.agent import run_research
from app.schemas import ResearchRequest, ResearchResponse

app = FastAPI(title="AI Research Assistant")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "AI Research Assistant backend is running"}


@app.post("/research", response_model=ResearchResponse)
async def research(req: ResearchRequest) -> ResearchResponse:
    return await run_research(req.question)
