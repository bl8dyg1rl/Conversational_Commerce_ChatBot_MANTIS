from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.conversation_context import ConversationContext

from app.services.llm_service import extract_intent

from app.services.recommendation_service import (
    get_recommended_products
)

from app.services.response_service import (
    generate_response
)


def get_or_create_conversation(
    db: Session,
    phone: str
) -> Conversation:

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.user_phone == phone
        )
        .first()
    )

    if conversation is None:

        conversation = Conversation(
            user_phone=phone
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    return conversation


def get_or_create_context(
    db: Session,
    conversation_id: int
) -> ConversationContext:

    context = (
        db.query(ConversationContext)
        .filter(
            ConversationContext.conversation_id
            == conversation_id
        )
        .first()
    )

    if context is None:

        context = ConversationContext(
            conversation_id=conversation_id
        )

        db.add(context)
        db.commit()
        db.refresh(context)

    return context


def update_context(
    context: ConversationContext,
    intent: dict
) -> ConversationContext:

    new_intent = intent.get("intent")

    new_product_type = intent.get(
        "product_type"
    )

    # =========================================================
    # INTENT
    # =========================================================

    if new_intent is not None:
        context.intent = new_intent

    # =========================================================
    # OCCASION
    # =========================================================

    if intent.get("occasion") is not None:

        context.occasion = intent["occasion"]

    # =========================================================
    # PRODUCT TYPE
    # =========================================================

    if new_product_type is not None:

        # Si el usuario está hablando de un producto
        # diferente al que tenía seleccionado,
        # eliminamos la selección anterior.
        if (
            context.product_type is not None
            and new_product_type.lower()
            != context.product_type.lower()
        ):

            context.selected_product_id = None

        context.product_type = new_product_type

    # =========================================================
    # PEOPLE
    # =========================================================

    if intent.get("people") is not None:

        context.people = intent["people"]

    # =========================================================
    # BUDGET
    # =========================================================

    if intent.get("budget") is not None:

        context.budget = intent["budget"]

    # =========================================================
    # QUANTITY
    # =========================================================

    if new_intent == "stock_check":

        if intent.get("quantity") is not None:

            context.quantity = intent["quantity"]

    else:

        context.quantity = None

    # =========================================================
    # PREFERENCE
    # =========================================================

    if intent.get("preference") is not None:

        context.preference = intent["preference"]

    return context


def save_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str
) -> Message:

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def process_chat_message(
    db: Session,
    phone: str,
    message: str
):

    conversation = get_or_create_conversation(
        db,
        phone
    )

    save_message(
        db,
        conversation.id,
        "user",
        message
    )

    context = get_or_create_context(
        db,
        conversation.id
    )

    intent = extract_intent(
        message
    )

    update_context(
        context,
        intent
    )

    db.commit()
    db.refresh(context)

    products = get_recommended_products(
        db,
        context
    )

    response = generate_response(
        db,
        context,
        products
    )

    save_message(
        db,
        conversation.id,
        "assistant",
        response
    )

    return (
        conversation,
        context,
        products,
        response
    )