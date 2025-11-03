import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()
os.getenv("DATABASE_URL", "sqlite:///./dev.db")

print("Loading .env file...")
print("PP_ENV", os.getenv("PP_ENV"))
print("PORT", os.getenv("PORT"))
print("DATABASE_URL", os.getenv("DATABASE_URL"))

app = FastAPI()


@app.get("/health")
async def root():
    return {"status": "ok"}
