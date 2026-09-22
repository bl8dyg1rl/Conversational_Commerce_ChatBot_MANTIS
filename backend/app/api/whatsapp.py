from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.products import get_db

from app.schemas.whatsapp import (
    WhatsAppWebhookRequest
)

from app.services.chat_service import (
    process_chat_message
)


router = APIRouter(
    prefix="/webhook",
    tags=["WhatsApp"]
)


VERIFY_TOKEN = "commerce_verify_token"


@router.get("/whatsapp")
async def verify_whatsapp_webhook(
    hub_mode: str | None = None,
    hub_verify_token: str | None = None,
    hub_challenge: str | None = None
):
    """
    Endpoint utilizado por Meta para verificar
    nuestro webhook.
    """

    if (
        hub_mode == "subscribe"
        and hub_verify_token == VERIFY_TOKEN
        and hub_challenge is not None
    ):
        return int(hub_challenge)

    return {
        "error": "Verification failed"
    }


@router.post("/whatsapp")
async def receive_whatsapp_message(
    data: WhatsAppWebhookRequest,
    db: Session = Depends(get_db)
):
    """
    Recibe un evento de WhatsApp y procesa
    el mensaje utilizando nuestro chatbot.
    """

    print("\n========== WHATSAPP WEBHOOK ==========")
    print(data.model_dump())
    print("======================================\n")

    try:

        if not data.entry:

            return {
                "status": "ignored",
                "reason": "No entry found"
            }

        value = (
            data.entry[0]
            ["changes"][0]
            ["value"]
        )

        messages = value.get(
            "messages",
            []
        )

        if not messages:

            return {
                "status": "ignored",
                "reason": "No message found"
            }

        message_data = messages[0]

        message_type = message_data.get(
            "type"
        )

        if message_type != "text":

            return {
                "status": "ignored",
                "reason": "Message is not text"
            }

        phone = message_data["from"]

        message_text = (
            message_data
            ["text"]
            ["body"]
        )

        print(
            f"📱 Usuario: {phone}"
        )

        print(
            f"💬 Mensaje: {message_text}"
        )

        (
            conversation,
            context,
            products
        ) = process_chat_message(
            db,
            phone,
            message_text
        )

        print(
            f"🧠 Intent: {context.intent}"
        )

        print(
            f"🛒 Productos encontrados: "
            f"{len(products)}"
        )

        return {
            "status": "processed",
            "phone": phone,
            "message": message_text,
            "conversation_id": conversation.id,
            "intent": context.intent,
            "response": "Mensaje procesado correctamente"
        }

    except Exception as error:

        print(
            "❌ Error procesando "
            "mensaje de WhatsApp:"
        )

        print(error)

        return {
            "status": "error",
            "message": str(error)
        }