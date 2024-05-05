from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, text, select
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

    def build_stack_as_list(self) -> list[str]:
        if self.stack is None:
            return []

        return self.stack.replace("{", "").replace("}", "").split(",")

    @classmethod
    @init_session
    def get_people_by_term(cls, term: str):
        query = text(
            f"""
            SELECT
                id, apelido, nome, nascimento, stack
            FROM pessoas
            WHERE
                apelido ILIKE '%{term}%'
                OR nome ILIKE '%{term}%'
                OR stack ILIKE '%{term}%'
            """
        )

        sql = select(Pessoa).from_statement(query)
        people = list(db_session.get().execute(sql).scalars())

        return people

    @classmethod
    @init_session
    def count(cls):
        return db_session.get().query(Pessoa).count()
