from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.product import Product


# ---------------------------------------------------------
# Diccionario de normalización
# ---------------------------------------------------------

TERM_MAPPING = {
    "hamburger": "hamburguesa",
    "hamburgers": "hamburguesa",
    "burger": "hamburguesa",
    "burgers": "hamburguesa",

    "bread": "pan",
    "breads": "pan",

    "cheese": "queso",
    "cheddar": "queso",

    "tomatoes": "tomate",
    "tomato": "tomate",

    "lettuce": "lechuga",

    "ketchup": "salsa",
    "sauces": "salsa",
    "sauce": "salsa",
}


def normalize_search_term(
    term: str
) -> str:

    term = term.lower().strip()

    return TERM_MAPPING.get(
        term,
        term
    )


def search_products(
    db: Session,
    query: str,
    limit: int = 20
) -> list[Product]:

    normalized_query = normalize_search_term(
        query
    )

    search_pattern = f"%{normalized_query}%"

    products = (
        db.query(Product)
        .filter(
            Product.stock > 0
        )
        .filter(
            or_(
                Product.name.ilike(search_pattern),
                Product.description.ilike(search_pattern),
                Product.category.ilike(search_pattern)
            )
        )
        .limit(limit)
        .all()
    )

    return products