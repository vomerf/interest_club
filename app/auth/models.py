
from typing import Optional
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    username: Mapped[str] = mapped_column(String(30))
    lastname: Mapped[Optional[str]]
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    security_question: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    security_answer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, lastname={self.lastname!r})"
