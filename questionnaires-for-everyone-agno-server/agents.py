from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from config import settings
from pydantic import BaseModel, Field

def get_model():
    """Returns the configured model based on LLM_PROVIDER."""
    if settings.LLM_PROVIDER == "google":
        return Gemini(id="gemini-2.0-flash", api_key=settings.GOOGLE_API_KEY)
    elif settings.LLM_PROVIDER == "openai":
        return OpenAIChat(id="gpt-4o", api_key=settings.OPENAI_API_KEY or settings.OPENAI_AUTH_KEY)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {settings.LLM_PROVIDER}")

class GEMBAResponse(BaseModel):
    score: int = Field(..., description="The translation quality score between 0 and 100.")

# Agent for GEMBA evaluation
gemba_agent = Agent(
    model=get_model(),
    instructions=[
        "You are an expert in evaluating translation quality using the GEMBA framework.",
        "Your goal is to provide a single score between 0 and 100 based on meaning preservation and grammar.",
    ],
    markdown=False,
    output_schema=GEMBAResponse,
    use_json_mode=True
)

class SSAResponse(BaseModel):
    score: str = Field(..., description="Semantic similarity score (0-100)")
    reasoning: str = Field(..., description="Justification for the score")
    suggestion: str = Field(..., description="Single paragraph suggesting changes")

# Agent for SSA (Semantic Similarity Assessment)
ssa_agent = Agent(
    model=get_model(),
    instructions=[
        "You are an expert in semantic similarity assessment.",
        "Evaluate the semantic similarity between two texts.",
        "Provide a score, reasoning, and suggestions for improvement.",
    ],
    markdown=False,
    output_schema=SSAResponse,
    use_json_mode=True
)
