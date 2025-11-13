import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session, select

from .database import get_session, init_db
from .models import (
    Task,
    TaskCreate,
    TaskPublic,
    TaskUpdate,
)
from .setup_logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    load_dotenv()
    setup_logging()
    init_db()
    logger = logging.getLogger(__name__)
    logger.info(f"PP_ENV: {os.getenv('PP_ENV')}")
    logger.info(f"PORT: {os.getenv('PORT')}")
    yield

    # Shutdown code (if any)


app = FastAPI(lifespan=lifespan)


# def hash_password(password):
# return f"hashed_{password}"


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
    # db_task is a Task, which will extract values from the TaskCreate object
    # and then update with info from extra_data dictionary, so including hashed_password
    # will not take password field as not defined in Task
    # extra_data takes precedence
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


## Add User Example
"""
@app.post("/users/", response_model=UserPublic)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = hash_password(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    # db_task is a Task, which will extract values from the TaskCreate object
    # and then update with info from extra_data dictionary, so including hashed_password
    # will not take password field as not defined in Task
    # extra_data takes precedence
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
    """
