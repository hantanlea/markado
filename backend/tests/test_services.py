"""Tests for markado.services using an in-memory SQLite database.

This module provides fixtures and tests for the markado.services
functions, including a Session fixture that sets up an in-memory SQLite
database for isolated testing.
"""

import pytest
from sqlmodel import Session, SQLModel, create_engine

from markado.models import Task
from markado.services import list_tasks


@pytest.fixture
def test_session():
    # Setup in-memory SQLite databtesting
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        echo=True,
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def session_with_tasks(test_session):
    tasks = [
        Task(name="Listen to French podcast"),
        Task(name="Learn sqlmodel"),
        Task(name="Buy bread"),
        Task(name="Clean floor"),
        Task(name="Finish setting up tests"),
    ]

    test_session.add_all(tasks)
    test_session.commit()
    return test_session


def test_list_tasks_empty_tasks(test_session):
    tasks = list_tasks(test_session)
    assert tasks == []


def test_list_tasks_with_tasks(session_with_tasks):
    tasks = list_tasks(session_with_tasks)
    assert len(tasks) == 5
    assert all(isinstance(t, Task) for t in tasks)
