from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.schemas import (
    AskRequest,
    AskResponse,
    ExplainRequest,
    ExplainResponse,
    QuizRequest,
    QuizResponse,
    LearningPathRequest,
    LearningPathResponse,
    SummarizeRequest,
    SummarizeResponse,
    StatusResponse,
)
from app.services.ai_service import ai_service

app = FastAPI(
    title="EduGenie API",
    description="Lightweight AI-powered educational assistant backend built with FastAPI.",
    version="1.0.0",
)

# Enable CORS for local development and client integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """Get system health and AI provider status."""
    return StatusResponse(
        status="active",
        ai_connected=ai_service.is_connected,
        model=settings.GEMINI_MODEL if ai_service.is_connected else "EduGenie Built-in Local Engine",
        features=[
            "Ask Q&A (Scenario 1)",
            "Concept Explainer",
            "Quiz Generator (Scenario 2)",
            "Personalized Learning Path (Scenario 3)",
            "Passage Summarizer",
        ],
    )


@app.post("/api/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """Scenario 1: Ask questions and receive smart, concise answers."""
    try:
        return await ai_service.ask_question(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/explain", response_model=ExplainResponse)
async def explain_concept(request: ExplainRequest):
    """Understand complex concepts through simplified explanations."""
    try:
        return await ai_service.explain_concept(request.concept, request.level)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/quiz", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    """Scenario 2: Generate quizzes from topics or text."""
    try:
        return await ai_service.generate_quiz(
            topic=request.topic,
            num_questions=request.num_questions,
            difficulty=request.difficulty,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/learning-path", response_model=LearningPathResponse)
async def get_learning_path(request: LearningPathRequest):
    """Scenario 3: Receive structured learning plan with beginner to advanced topics, timelines, and suggestions."""
    try:
        return await ai_service.get_learning_path(
            topic=request.topic,
            target_level=request.target_level,
            timeframe=request.timeframe,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize_passage(request: SummarizeRequest):
    """Summarize large educational passages into key takeaways."""
    try:
        return await ai_service.summarize_passage(request.text, request.format)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve static files for the frontend
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(str(STATIC_DIR / "index.html"))
