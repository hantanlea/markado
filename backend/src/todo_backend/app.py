import os

from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

print("Loading .env file...")
print("PP_ENV", os.getenv("PP_ENV"))
print("PORT", os.getenv("PORT"))

app = FastAPI()


@app.get("/health")
async def root() -> dict[str, str]:
    return {"status": "ok"}
