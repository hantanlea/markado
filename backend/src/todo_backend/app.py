import os

from dotenv import load_dotenv
from fastapi import FastAPI

from .database import create_db_and_tables

load_dotenv()

print("Loading .env file...")
print("PP_ENV", os.getenv("PP_ENV"))
print("PORT", os.getenv("PORT"))

app = FastAPI()


@app.get("/health")
async def root() -> dict[str, str]:
    return {"status": "ok"}


def create_tasks() -> None:
    return


def main() -> None:
    create_db_and_tables()
    create_tasks()


if __name__ == "__main__":
    main()
