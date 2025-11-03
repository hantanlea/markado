import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()
# os.getenv("DATABASE_URL", "sqlite:///./dev.db")

print("Using database:", os.getenv("DATABASE_URL"))

# sqlite_file_name = "database.db"
sqlite_url = os.getenv("DATABASE_URL") or "sqlite://./dev.db"

engine = create_engine(sqlite_url)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
