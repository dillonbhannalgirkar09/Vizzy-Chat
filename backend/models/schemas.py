from pydantic import BaseModel
from typing import List, Optional, Literal, Union, Dict, Any

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    type: Literal["text", "images", "hybrid"]
    data: Union[str, List[str], Dict[str, Any]]  # Can be string, list of strings, or dict
    metadata: Optional[dict] = {}