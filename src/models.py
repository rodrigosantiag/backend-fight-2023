from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, LocalSession
from database.db_session import DBSession
from redis import StrictRedis

db_session = DBSession()


def get_session():
    session = LocalSession()

    try:
        yield session
    finally:
        session.close()


def get_redis():  # pragma: no cover
    return StrictRedis(host="redis", port=6379, decode_responses=True)


def init_session(func):
    def decorator(*args, **kwargs):
        db_session.create()
        result = func(*args, **kwargs)
        return result

    return decorator


class Pessoa(Base):
    __tablename__ = "pessoas"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    apelido: Mapped[str] = mapped_column(String(32), unique=True)
    nome: Mapped[str] = mapped_column(String(100))
    nascimento: Mapped[date]
    stack: Mapped[Optional[str]]

    def build_stack_as_list(self) -> list[str]:
        if self.stack is None:
            return []

        return self.stack.replace("{", "").replace("}", "").split(",")
