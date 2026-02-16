from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DB_PATH

# SQLite connection string
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Engine = connection to database
engine = create_engine(
    DATABASE_URL,
    echo=True  # shows SQL in terminal (great for learning)
)

# Session replaces cursor
SessionLocal = sessionmaker(bind=engine)

# Base class for all tables
Base = declarative_base()