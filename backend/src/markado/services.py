"""Services for interacting with Task models in the todo backend.

This module provides helper functions that operate on the database via SQLModel
sessions, such as listing, creating, and updating Task records.
"""

from typing import cast

from sqlmodel import Session, select

from markado.database import engine
from markado.models import Task, TaskCreate, TaskUpdate


def list_tasks(session: Session, *, offset: int = 0, limit: int = 100) -> list[Task]:
    """Retrieve a list of Task records from the database."""
    result = session.exec(select(Task).offset(offset).limit(limit))
    tasks = cast(list[Task], result.all())
    return tasks


def get_task(session: Session, task_id: int) -> Task | None:
    """Retrieve a single Task by its ID."""
    task = session.get(Task, task_id)
    return task


def create_task(session: Session, task_create: TaskCreate) -> Task:
    """Create a new Task record in the database."""
    db_task = Task.model_validate(task_create)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int) -> bool:
    """Delete a Task record from the database by its ID."""
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    else:
        return False


def update_task(session: Session, task_id: int, task_update: TaskUpdate) -> Task | None:
    """Update an existing Task record in the database."""
    db_task = session.get(Task, task_id)
    if not db_task:
        return None
    task_data = task_update.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


if __name__ == "__main__":
    with Session(engine) as session:
        print(list_tasks(session))
