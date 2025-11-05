import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from .database import get_session
from .models import (
    Task,
    TaskCreate,
    TaskPublic,
    TaskUpdate,
)

load_dotenv()

print("Loading .env file...")
print("PP_ENV", os.getenv("PP_ENV"))
print("PORT", os.getenv("PORT"))

app = FastAPI()


@app.get("/health")
async def root() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/tasks/", response_model=list[TaskPublic])
def list_tasks(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()

    return tasks


@app.get("/tasks/{task_id}", response_model=TaskPublic)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks/", response_model=TaskPublic)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return None


@app.patch("/tasks/{task_id}", response_model=TaskPublic)
def update_task(
    task_id: int, task: TaskUpdate, session: Session = Depends(get_session)
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    # this returns a dictionary of only the data sent by the client
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
