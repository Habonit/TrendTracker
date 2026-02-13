from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings
import os

# SQLite DB Path (data/trend_tracker.db)
DB_PATH = os.path.join("data", "trend_tracker.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} # Required for SQLite + multiple threads (Streamlit)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
