import csv
import os

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.product import Product


CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "products.csv"
)


def import_products():

    db: Session = SessionLocal()

    created = 0
    updated = 0

    try:

        with open(
            CSV_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                product = (
                    db.query(Product)
                    .filter(
                        Product.name == row["name"]
                    )
                    .first()
                )

                if product is None:

                    product = Product(
                        name=row["name"],
                        description=row["description"],
                        category=row["category"],
                        price=float(row["price"]),
                        stock=int(row["stock"]),
                        unit=row["unit"],
                        brand=row["brand"] or None
                    )

                    db.add(product)

                    created += 1

                else:

                    product.description = (
                        row["description"]
                    )

                    product.category = (
                        row["category"]
                    )

                    product.price = (
                        float(row["price"])
                    )

                    product.stock = (
                        int(row["stock"])
                    )

                    product.unit = (
                        row["unit"]
                    )

                    product.brand = (
                        row["brand"] or None
                    )

                    updated += 1

        db.commit()

        print(
            f"Importación completada."
        )

        print(
            f"Productos creados: {created}"
        )

        print(
            f"Productos actualizados: {updated}"
        )

    except Exception as error:

        db.rollback()

        print(
            "Error al importar productos:"
        )

        print(error)

    finally:

        db.close()


if __name__ == "__main__":
    import_products()