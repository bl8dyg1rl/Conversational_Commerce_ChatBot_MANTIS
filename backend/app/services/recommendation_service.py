from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.conversation_context import ConversationContext

from app.services.search_service import search_products


def get_recommended_products(
    db: Session,
    context: ConversationContext,
    limit: int = 10
) -> list[Product]:

    # -----------------------------------------
    # CASE 1: SPECIFIC PRODUCT
    # -----------------------------------------

    if context.product_type:

        products = search_products(
            db,
            context.product_type,
            limit=limit
        )

        if context.budget is not None:

            budget = float(context.budget)

            products = [
                product
                for product in products
                if float(product.price) <= budget
            ]

        products.sort(
            key=lambda product: float(product.price)
        )

        return products

    # -----------------------------------------
    # CASE 2: GENERAL RECOMMENDATION
    # -----------------------------------------

    if context.intent == "product_recommendation":

        products = (
            db.query(Product)
            .filter(
                Product.stock > 0
            )
            .limit(limit)
            .all()
        )

        if context.budget is not None:

            budget = float(context.budget)

            products = [
                product
                for product in products
                if float(product.price) <= budget
            ]

        products.sort(
            key=lambda product: float(product.price)
        )

        return products

    return []