from typing import List, Optional
from pydantic import BaseModel, Field


# --- Ask Q&A (Scenario 1) ---
class AskRequest(BaseModel):
    question: str = Field(..., description="Educational question to ask EduGenie", min_length=2)


class AskResponse(BaseModel):
    question: str
    answer: str
    key_points: List[str] = Field(default_factory=list)
    suggested_followups: List[str] = Field(default_factory=list)
    source_model: str = "EduGenie AI"


# --- Concept Simplifier ---
class ExplainRequest(BaseModel):
    concept: str = Field(..., description="Concept to simplify and explain", min_length=2)
    level: str = Field(default="simple", description="'simple' (ELI5), 'high_school', or 'advanced'")


class ExplainResponse(BaseModel):
    concept: str
    level: str
    summary: str
    simple_analogy: str
    detailed_explanation: str
    real_world_example: str
    source_model: str = "EduGenie AI"


# --- Quiz Generator (Scenario 2) ---
class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_answer_index: int
    explanation: str


class QuizRequest(BaseModel):
    topic: str = Field(..., description="Topic or passage to generate a quiz from", min_length=2)
    num_questions: int = Field(default=3, ge=1, le=10)
    difficulty: str = Field(default="medium", description="'easy', 'medium', or 'hard'")


class QuizResponse(BaseModel):
    topic: str
    difficulty: str
    questions: List[QuizQuestion]
    source_model: str = "EduGenie AI"


# --- Learning Path (Scenario 3) ---
class LearningPhase(BaseModel):
    phase_name: str
    duration: str
    topics: List[str]
    hands_on_project: str
    resources: List[str] = Field(default_factory=list)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., description="Topic or technology to build a roadmap for", min_length=2)
    target_level: str = Field(default="advanced", description="'intermediate' or 'advanced'")
    timeframe: str = Field(default="4-6 weeks")


class LearningPathResponse(BaseModel):
    topic: str
    overview: str
    estimated_total_time: str
    phases: List[LearningPhase]
    pro_tips: List[str] = Field(default_factory=list)
    source_model: str = "EduGenie AI"


# --- Summarizer ---
class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Educational passage to summarize", min_length=20)
    format: str = Field(default="bullet", description="'bullet', 'tldr', or 'in_depth'")


class SummarizeResponse(BaseModel):
    original_word_count: int
    summary_word_count: int
    summary: str
    key_takeaways: List[str]
    reading_time_saved: str
    source_model: str = "EduGenie AI"


# --- Status ---
class StatusResponse(BaseModel):
    status: str
    ai_connected: bool
    model: str
    features: List[str]
