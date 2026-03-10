from fastapi import FastAPI
from app.schemas import ResearchRequest
from app.agent import run_research

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "AI Research Assistant backend is running"}


@app.post("/research")
async def research(req: ResearchRequest):
    result = await run_research(req.question)
    return result