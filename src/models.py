from datetime import date
from typing import Optional
from uuid import UUID


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Pessoa(Base):
    __tablename__ = "pessoas"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    apelido: Mapped[str] = mapped_column(String(32))
    nome: Mapped[str] = mapped_column(String(100))
    nascimento: Mapped[date]
    stack: Mapped[Optional[str]]
