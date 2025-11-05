import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from .database import get_session
from .models import Task

load_dotenv()

print("Loading .env file...")
print("PP_ENV", os.getenv("PP_ENV"))
print("PORT", os.getenv("PORT"))

app = FastAPI()


@app.get("/health")
async def root() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks/", response_model=list[Task])
def list_tasks(session: Session = Depends(get_session)):
    """Returns all tasks from the database."""
    tasks = session.exec(select(Task)).all()
    return tasks


@app.post("/tasks/", response_model=Task)
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return None
