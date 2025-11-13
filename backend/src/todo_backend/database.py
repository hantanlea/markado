import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]
db_path = Path(f"{BASE_DIR}/{os.getenv('DATABASE_PATH', './data')}")
sqlite_url = f"sqlite:///{db_path}"

# intialise sqlmodel engine
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def init_db() -> None:
    """Initializes the database."""
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        logger.info("Database connection successful.")
        logger.info(f"Connected to: {sqlite_url} at {db_path}")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


def create_db_and_tables() -> None:
    logger.info(f"Creating database tables at {sqlite_url}")
    SQLModel.metadata.create_all(engine)


def get_session():
    # Dependency that opens a new DB session for each request.
    # Uses 'yield' so FastAPI can pause here, run the endpoint with the open session,
    # then resume afterwards to exit the with block and close the session.
    # Using 'return' would close too early.
    with Session(engine) as session:
        yield session
