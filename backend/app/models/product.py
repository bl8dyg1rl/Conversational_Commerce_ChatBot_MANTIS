from sqlalchemy import String, Text, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    brand: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )