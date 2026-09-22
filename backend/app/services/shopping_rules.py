import math


# ---------------------------------------------------------
# Reglas para preparar hamburguesas
# ---------------------------------------------------------

HAMBURGER_RULES = {
    "hamburguesa": {
        "hamburguesa de res": 1,
        "pan de hamburguesa": 1 / 8,
        "queso cheddar": 1 / 8,
        "tomate": 1 / 5,
        "lechuga": 1 / 10,
        "salsa de tomate": 1 / 25,
    }
}


def calculate_required_quantity(
    product_name: str,
    people: int,
    product_unit: str
) -> int:

    product_name_normalized = (
        product_name.lower().strip()
    )

    # ---------------------------------------------------------
    # Hamburguesa de res
    # ---------------------------------------------------------

    if product_name_normalized == "hamburguesa de res":

        return people

    # ---------------------------------------------------------
    # Pan de hamburguesa
    # 1 paquete = aproximadamente 8 panes
    # ---------------------------------------------------------

    if product_name_normalized == "pan de hamburguesa":

        return max(
            1,
            math.ceil(people / 8)
        )

    # ---------------------------------------------------------
    # Queso cheddar
    # 1 paquete = aproximadamente 8 tajadas
    # ---------------------------------------------------------

    if product_name_normalized == "queso cheddar":

        return max(
            1,
            math.ceil(people / 8)
        )

    # ---------------------------------------------------------
    # Tomate
    # 1 tomate por cada 5 personas
    # ---------------------------------------------------------

    if product_name_normalized == "tomate":

        return max(
            1,
            math.ceil(people / 5)
        )

    # ---------------------------------------------------------
    # Lechuga
    # 1 lechuga por cada 10 personas
    # ---------------------------------------------------------

    if product_name_normalized == "lechuga":

        return max(
            1,
            math.ceil(people / 10)
        )

    # ---------------------------------------------------------
    # Salsa
    # 1 botella por cada 25 personas
    # ---------------------------------------------------------

    if product_name_normalized == "salsa de tomate":

        return max(
            1,
            math.ceil(people / 25)
        )

    return 1