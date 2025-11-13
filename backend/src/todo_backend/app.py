import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Session

from todo_backend import services

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
def list_tasks_endpoint(
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> list[Task]:
    """Return a paginated list of tasks."""
    return services.list_tasks(session, offset=offset, limit=limit)


@app.get("/tasks/{task_id}", response_model=TaskPublic)
def get_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    task = services.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks/", response_model=TaskPublic)
def create_task_endpoint(
    task_create: TaskCreate, session: Session = Depends(get_session)
):
    return services.create_task(session, task_create)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session)) -> None:
    deleted = services.delete_task(session, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@app.patch("/tasks/{task_id}", response_model=TaskPublic)
def update_task_endpoint(
    task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)
):
    updated_task = services.update_task(session, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


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
