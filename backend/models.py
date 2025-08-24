"""Pydantic models for API requests and responses."""

from pydantic import BaseModel, Field
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    content: str
    tokens: int
    cost: float

class ChallengeRequest(BaseModel):
    message: str
    user_id: str
    conversation_id: str

class AgentWorkflow(BaseModel):
    agent: str
    decision: str = ""

class ChallengeResponse(BaseModel):
    response: str
    source_agent_response: str
    agent_workflow: List[AgentWorkflow]