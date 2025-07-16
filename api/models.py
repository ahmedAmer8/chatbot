
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChatMessage(BaseModel):
    """Model for a single chat message"""
    role: str
    content: str

class ChatRequest(BaseModel):
    """Model for chat request"""
    message: str
    conversation_history: Optional[List[ChatMessage]] = None

class ChatResponse(BaseModel):
    """Model for chat response"""
    response: str
    tokens_used: int
    execution_time: float
    success: bool