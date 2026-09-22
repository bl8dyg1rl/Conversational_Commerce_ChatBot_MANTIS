from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest, ChatResponse

from app.services.chat_service import (
    process_chat_message
)

from app.api.products import get_db


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    (
        conversation,
        context,
        products,
        response
    ) = process_chat_message(
        db,
        request.phone,
        request.message
    )

    return ChatResponse(
        conversation_id=conversation.id,
        response=response
    )