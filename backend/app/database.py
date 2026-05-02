from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

# Use MySQL by default. Set USE_SQLITE=true for SQLite (development without MySQL server)
USE_SQLITE = os.environ.get("USE_SQLITE", "false").lower() == "true"

if USE_SQLITE:
    # SQLite - works without any server. Use absolute path so DB is always
    # in the backend directory regardless of process CWD.
    _backend_dir = os.path.dirname(os.path.abspath(__file__))
    SQLITE_PATH = os.path.join(_backend_dir, "text_summarizer.db")
    DATABASE_URL = f"sqlite:///{SQLITE_PATH.replace(os.sep, '/')}"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False, "timeout": 15},  # SQLite specific
        echo=False
    )
    print(f"Using SQLite database: {SQLITE_PATH}")
else:
    # MySQL - requires MySQL server running
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False
        )
        # Test connection
        with engine.connect() as conn:
            pass
        print("Connected to MySQL database")
    except Exception as e:
        print(f"MySQL connection failed: {e}")
        print("Falling back to SQLite...")
        _backend_dir = os.path.dirname(os.path.abspath(__file__))
        SQLITE_PATH = os.path.join(_backend_dir, "text_summarizer.db")
        DATABASE_URL = f"sqlite:///{SQLITE_PATH.replace(os.sep, '/')}"
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=False
        )
        print(f"Using SQLite database: {SQLITE_PATH}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
