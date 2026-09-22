from sqlalchemy.orm import Session

from app.models.conversation_context import ConversationContext
from app.models.product import Product

from app.services.search_service import search_products


def get_selected_product(
    db: Session,
    context: ConversationContext
) -> Product | None:

    if context.selected_product_id is None:
        return None

    return (
        db.query(Product)
        .filter(
            Product.id == context.selected_product_id
        )
        .first()
    )


def generate_response(
    db: Session,
    context: ConversationContext,
    recommended_products: list[Product]
) -> str:

    intent = context.intent

    # =========================================================
    # PRODUCT RECOMMENDATION
    # =========================================================

    if intent == "product_recommendation":

        products = recommended_products

        if not products:

            return (
                "No encontré productos disponibles "
                "relacionados con lo que estás buscando."
            )

        if context.product_type:

            title = (
                "🛒 Estos son los productos "
                "que encontré para "
                f"{context.product_type}:"
            )

        elif context.occasion:

            title = (
                "🛒 Estos son algunos productos "
                "disponibles para tu "
                f"{context.occasion}:"
            )

        else:

            title = (
                "🛒 Estos son algunos productos "
                "que tenemos disponibles:"
            )

        lines = [
            title,
            ""
        ]

        for product in products:

            lines.append(
                f"• {product.name} — "
                f"${float(product.price):,.0f} "
                f"por {product.unit}"
            )

        return "\n".join(lines)

    # =========================================================
    # PRODUCT SEARCH
    # =========================================================

    if intent == "product_search":

        # Si ya existe un producto seleccionado,
        # mostramos directamente ese producto.
        selected_product = get_selected_product(
            db,
            context
        )

        if selected_product is not None:

            return (
                f"🔎 {selected_product.name}\n\n"
                f"Precio: "
                f"${float(selected_product.price):,.0f} "
                f"por {selected_product.unit}\n"
                f"Disponibles: "
                f"{selected_product.stock}"
            )

        if not context.product_type:

            return (
                "Claro 😊 ¿Qué producto estás buscando?"
            )

        products = search_products(
            db,
            context.product_type
        )

        if not products:

            return (
                f"No encontré "
                f"'{context.product_type}' "
                "en nuestro catálogo."
            )

        if len(products) == 1:

            product = products[0]

            return (
                f"🔎 Encontré "
                f"{product.name}.\n\n"
                f"Precio: "
                f"${float(product.price):,.0f} "
                f"por {product.unit}\n"
                f"Disponibles: "
                f"{product.stock}"
            )

        lines = [
            "🔎 Encontré varios productos "
            "que coinciden:",
            ""
        ]

        for product in products:

            lines.append(
                f"• {product.name} — "
                f"${float(product.price):,.0f} "
                f"por {product.unit}"
            )

        lines.append("")
        lines.append(
            "Selecciona uno de los productos "
            "para continuar:"
        )

        return "\n".join(lines)

    # =========================================================
    # STOCK CHECK
    # =========================================================

    if intent == "stock_check":

        # Si el usuario ya seleccionó un producto,
        # usamos directamente ese producto.
        selected_product = get_selected_product(
            db,
            context
        )

        if selected_product is not None:

            product = selected_product

            if context.quantity is None:

                return (
                    f"📦 Tenemos "
                    f"{product.stock} "
                    f"{product.unit} disponibles "
                    f"de {product.name}."
                )

            requested_quantity = context.quantity

            if product.stock >= requested_quantity:

                return (
                    f"✅ Sí, tenemos "
                    f"{requested_quantity} "
                    f"{product.unit} de "
                    f"{product.name}.\n\n"
                    f"Stock actual: "
                    f"{product.stock}."
                )

            return (
                f"❌ No tenemos "
                f"{requested_quantity} "
                f"{product.unit} de "
                f"{product.name}.\n\n"
                f"Actualmente tenemos "
                f"{product.stock} disponibles."
            )

        # -----------------------------------------------------
        # No existe producto seleccionado.
        # Buscamos por product_type.
        # -----------------------------------------------------

        if not context.product_type:

            return (
                "Claro 😊 ¿De qué producto "
                "quieres consultar la disponibilidad?"
            )

        products = search_products(
            db,
            context.product_type
        )

        if not products:

            return (
                f"No encontré "
                f"'{context.product_type}' "
                "en nuestro catálogo."
            )

        if len(products) > 1:

            lines = [
                "Encontré varios productos "
                "que coinciden:",
                ""
            ]

            for product in products:

                lines.append(
                    f"• {product.name}"
                )

            lines.append("")
            lines.append(
                "Selecciona uno de los productos "
                "para consultar su disponibilidad:"
            )

            return "\n".join(lines)

        product = products[0]

        if context.quantity is None:

            return (
                f"📦 Tenemos "
                f"{product.stock} "
                f"{product.unit} disponibles "
                f"de {product.name}."
            )

        requested_quantity = context.quantity

        if product.stock >= requested_quantity:

            return (
                f"✅ Sí, tenemos "
                f"{requested_quantity} "
                f"{product.unit} de "
                f"{product.name}.\n\n"
                f"Stock actual: "
                f"{product.stock}."
            )

        return (
            f"❌ No tenemos "
            f"{requested_quantity} "
            f"{product.unit} de "
            f"{product.name}.\n\n"
            f"Actualmente tenemos "
            f"{product.stock} disponibles."
        )

    # =========================================================
    # GENERAL QUESTION
    # =========================================================

    if intent == "general_question":

        return (
            "¡Hola! 👋 Puedo ayudarte a encontrar "
            "productos de nuestro catálogo y consultar "
            "su disponibilidad. ¿Qué estás buscando?"
        )

    # =========================================================
    # UNKNOWN
    # =========================================================

    return (
        "No estoy seguro de haber entendido "
        "lo que necesitas 😅. Puedes decirme "
        "qué producto estás buscando o qué "
        "necesitas comprar."
    )