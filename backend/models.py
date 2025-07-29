from pydantic import BaseModel
from typing import Optional, List

# Core data models
class Source(BaseModel):
    """A source citation with title and URL"""
    title: str
    url: str

class PerplexityResponse(BaseModel):
    """Structured response model for Perplexity AI clone"""
    summary: str
    explore_more: List[Source]

# API request/response models
class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: PerplexityResponse
    thread_id: str

class HealthResponse(BaseModel):
    status: str
    message: str 