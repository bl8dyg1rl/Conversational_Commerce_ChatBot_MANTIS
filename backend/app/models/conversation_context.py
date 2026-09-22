from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ConversationContext(Base):
    __tablename__ = "conversation_contexts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False,
        unique=True
    )

    intent: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    occasion: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    product_type: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    selected_product_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    people: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    budget: Mapped[float | None] = mapped_column(
        Numeric(12, 2),
        nullable=True
    )

    quantity: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    preference: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    conversation = relationship(
        "Conversation",
        back_populates="context"
    )