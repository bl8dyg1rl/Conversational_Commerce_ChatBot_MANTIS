from fastapi import FastAPI

from app.core.database import Base, engine

from app.models.product import Product
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.conversation_context import ConversationContext

from app.api.products import router as products_router
from app.api.chat import router as chat_router
from app.api.whatsapp import router as whatsapp_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Conversational Commerce API",
    description="AI-powered product recommendation engine",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Conversational Commerce API is running"
    }


app.include_router(
    products_router,
    prefix="/products"
)

app.include_router(
    chat_router
)

app.include_router(
    whatsapp_router
)