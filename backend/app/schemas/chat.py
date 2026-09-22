from pydantic import BaseModel


class ChatRequest(BaseModel):
    phone: str
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
