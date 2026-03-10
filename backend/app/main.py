from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ResearchRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return {"message": "AI Research Assistant backend is running"}


@app.post("/research")
async def research(req: ResearchRequest):
    return {
        "question": req.question,
        "result": "This is a placeholder research result."
    }