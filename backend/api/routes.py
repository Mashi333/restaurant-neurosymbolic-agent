from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.chatbot_service import handle_chat

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    context: dict

class ChatResponse(BaseModel):
    response: str
    reasoning: dict

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    response, reasoning = handle_chat(req.message, req.context)
    return ChatResponse(response=response, reasoning=reasoning)
