import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

# initialise database
load_dotenv()
print("Using database:", os.getenv("DATABASE_URL"))
sqlite_url = os.getenv("DATABASE_URL") or "sqlite://./dev.db"

# intialise sqlmodel engine
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    # Dependency that opens a new DB session for each request.
    # Uses 'yield' so FastAPI can pause here, run the endpoint with the open session,
    # then resume afterwards to exit the with block and close the session.
    # Using 'return' would close too early.
    with Session(engine) as session:
        yield session
