from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from database.db_session import DBSession

db_session = DBSession()


def get_session():
    db_session.create()

    try:
        yield db_session.get()
    except Exception as exc:
        db_session.rollback()
        raise exc
    finally:
        db_session.close()


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
