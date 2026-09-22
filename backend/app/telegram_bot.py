import socket

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from app.core.config import settings
from app.core.database import SessionLocal

from app.services.chat_service import (
    process_chat_message
)


INSTANCE_LOCK_HOST = "127.0.0.1"
INSTANCE_LOCK_PORT = 47651
_instance_lock = None


def acquire_instance_lock() -> bool:
    global _instance_lock

    _instance_lock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        _instance_lock.bind(
            (INSTANCE_LOCK_HOST, INSTANCE_LOCK_PORT)
        )
        return True
    except OSError:
        _instance_lock.close()
        _instance_lock = None
        return False


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Recibe un mensaje de Telegram y lo envía
    al cerebro del chatbot.
    """

    if update.message is None:
        return

    if update.message.text is None:
        return

    message_text = update.message.text

    telegram_user = update.effective_user

    if telegram_user is None:
        return

    phone = f"telegram_{telegram_user.id}"

    print("\n========== TELEGRAM ==========")

    print(
        f"👤 Usuario: "
        f"{telegram_user.first_name}"
    )

    print(
        f"💬 Mensaje: "
        f"{message_text}"
    )

    db = SessionLocal()

    try:

        (
            conversation,
            context_data,
            products,
            response
        ) = process_chat_message(
            db,
            phone,
            message_text
        )

        print(
            f"🧠 Intent: "
            f"{context_data.intent}"
        )

        print(
            f"🛒 Productos encontrados: "
            f"{len(products)}"
        )

        print(
            f"🤖 Respuesta: "
            f"{response}"
        )

        # Si encontramos varios productos,
        # mostramos botones para que el usuario
        # pueda seleccionar uno.
        if (
            context_data.intent in [
                "product_search",
                "stock_check"
            ]
            and len(products) > 1
        ):

            keyboard = []

            for product in products:

                keyboard.append(
                    [
                        InlineKeyboardButton(
                            text=product.name,
                            callback_data=f"product:{product.id}"
                        )
                    ]
                )

            reply_markup = InlineKeyboardMarkup(
                keyboard
            )

            await update.message.reply_text(
                response,
                reply_markup=reply_markup
            )

        else:

            await update.message.reply_text(
                response
            )

    except Exception as error:

        print(
            "❌ Error procesando mensaje:"
        )

        print(error)

        await update.message.reply_text(
            "Ocurrió un error procesando "
            "tu mensaje 😕."
        )

    finally:

        db.close()

    print("===============================\n")


async def handle_product_selection(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Procesa cuando el usuario selecciona
    un producto mediante un botón.
    """

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    callback_data = query.data

    if callback_data is None:
        return

    if not callback_data.startswith("product:"):
        return

    product_id = int(
        callback_data.split(":")[1]
    )

    telegram_user = query.from_user

    phone = f"telegram_{telegram_user.id}"

    db = SessionLocal()

    try:

        from app.models.product import Product
        from app.models.conversation_context import (
            ConversationContext
        )
        from app.models.conversation import Conversation
        from app.models.message import Message

        # Buscar la conversación del usuario
        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.user_phone == phone
            )
            .first()
        )

        if conversation is None:

            await query.edit_message_text(
                "No encontré tu conversación."
            )

            return

        # Buscar el producto seleccionado
        product = (
            db.query(Product)
            .filter(
                Product.id == product_id
            )
            .first()
        )

        if product is None:

            await query.edit_message_text(
                "Ese producto ya no está disponible."
            )

            return

        # Buscar el contexto actual
        context_data = (
            db.query(ConversationContext)
            .filter(
                ConversationContext.conversation_id
                == conversation.id
            )
            .first()
        )

        if context_data is None:

            await query.edit_message_text(
                "No encontré el contexto de la conversación."
            )

            return

        # Guardamos el producto seleccionado
        context_data.selected_product_id = (
            product.id
        )

        # También actualizamos el tipo de producto
        context_data.product_type = (
            product.name
        )

        db.commit()

        # Guardamos la selección como mensaje
        selection_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=f"[Producto seleccionado] {product.name}"
        )

        db.add(selection_message)
        db.commit()

        response = (
            f"✅ Has seleccionado:\n\n"
            f"🛒 {product.name}\n\n"
            f"Precio: "
            f"${float(product.price):,.0f} "
            f"por {product.unit}\n"
            f"Disponibles: "
            f"{product.stock}"
        )

        await query.edit_message_text(
            response
        )

        print(
            "\n========== PRODUCTO SELECCIONADO =========="
        )

        print(
            f"👤 Usuario: "
            f"{telegram_user.first_name}"
        )

        print(
            f"🛒 Producto: "
            f"{product.name}"
        )

        print(
            f"🆔 Product ID: "
            f"{product.id}"
        )

        print(
            "============================================\n"
        )

    except Exception as error:

        db.rollback()

        print(
            "❌ Error seleccionando producto:"
        )

        print(error)

        await query.edit_message_text(
            "Ocurrió un error seleccionando "
            "el producto 😕."
        )

    finally:

        db.close()


def main():

    if not acquire_instance_lock():

        print(
            "El bot de Telegram ya está ejecutándose. "
            "Cierra la otra instancia antes de iniciar esta."
        )

        return

    application = (
        Application
        .builder()
        .token(
            settings.telegram_bot_token
        )
        .build()
    )

    # Mensajes normales
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    # Botones de selección de productos
    application.add_handler(
        CallbackQueryHandler(
            handle_product_selection,
            pattern=r"^product:"
        )
    )

    print(
        "🤖 Telegram bot iniciado."
    )

    print(
        "Esperando mensajes..."
    )

    application.run_polling()


if __name__ == "__main__":
    main()