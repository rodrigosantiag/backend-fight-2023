import os

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine(
    os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://postgres:password@localhost:15432/backend_fight_2023"
    ),
    pool_size=20,
    max_overflow=0,
)

LocalSession = sessionmaker(engine, expire_on_commit=False)
