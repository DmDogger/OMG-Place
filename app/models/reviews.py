from sqlalchemy import Boolean, Integer, Text, DateTime, CheckConstraint, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import datetime

class Review(Base):
    __tablename__ = 'reviews'

    __table_args__ = (
        CheckConstraint('grade >= 1 AND grade <=5',
                        name='check_grade'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped['User'] = relationship(
        back_populates='comments'
    )

    product: Mapped['Product'] = relationship(
        back_populates='comments'
    )
