import os

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine(
    os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://postgres:password@localhost:15432/backend_fight_2023"
    ),
    pool_size=100,
    max_overflow=40,
)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
