"""Tests for markado.services using an in-memory SQLite database.

This module provides fixtures and tests for the markado.services
functions, including a Session fixture that sets up an in-memory SQLite
database for isolated testing.
"""

import pytest
from sqlmodel import Session, SQLModel, create_engine, select

from markado.models import Task, TaskCreate, TaskUpdate
from markado.services import create_task, delete_task, get_task, list_tasks, update_task

## list-tasks tests


@pytest.fixture
def test_session():
    # Setup in-memory SQLite database for testing
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        echo=False,
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def session_with_tasks(test_session: Session):
    tasks = [
        Task(name="T1"),
        Task(name="T2"),
        Task(name="T3"),
        Task(name="T4"),
        Task(name="T5"),
    ]

    test_session.add_all(tasks)
    test_session.commit()
    return test_session


@pytest.fixture
def make_tasks(test_session: Session):
    def _make_tasks(count: int):
        for i in range(count):
            task = Task(name=f"T{i + 1}")
            test_session.add(task)
        test_session.commit()

    return _make_tasks


## Tests for list-tasks


def test_list_tasks_empty_tasks(test_session):
    tasks = list_tasks(test_session)
    assert tasks == []


def test_list_tasks_small_db(make_tasks, test_session):
    make_tasks(5)
    tasks = list_tasks(test_session)
    assert len(tasks) == 5
    assert tasks[0].name == "T1"
    assert tasks[1].name == "T2"
    assert tasks[-1].name == "T5"
    assert all(isinstance(t, Task) for t in tasks)


@pytest.mark.parametrize(
    "offset, limit, expected",
    [
        pytest.param(0, 100, ["T1", "T2", "T3", "T4", "T5"], id="defaults_0_100"),
        pytest.param(1, 100, ["T2", "T3", "T4", "T5"], id="offset_1_limit_100"),
        pytest.param(0, 2, ["T1", "T2"], id="offset_0_limit_2"),
        pytest.param(2, 3, ["T3", "T4", "T5"], id="offset_2_limit_3"),
        pytest.param(5, 10, [], id="offset=length"),
        pytest.param(0, 0, [], id="limit=0"),
        pytest.param(0, 999, ["T1", "T2", "T3", "T4", "T5"], id="offset_0_limit_999"),
    ],
)
def test_list_tasks_pagination_small_db(offset, limit, expected, session_with_tasks):
    tasks = list_tasks(session_with_tasks, offset=offset, limit=limit)
    tasks_names = [task.name for task in tasks]
    assert tasks_names == expected


def test_list_tasks_large_db_defaults(make_tasks, test_session):
    make_tasks(150)
    tasks = list_tasks(test_session)  # offset = 0, limit = 100
    assert len(tasks) == 100
    assert tasks[0].name == "T1"
    assert tasks[1].name == "T2"
    assert tasks[-1].name == "T100"
    assert all(isinstance(t, Task) for t in tasks)


def test_list_tasks_large_db_offset(make_tasks, test_session):
    make_tasks(150)
    tasks = list_tasks(test_session, offset=50, limit=100)
    assert len(tasks) == 100
    assert tasks[0].name == "T51"
    assert tasks[1].name == "T52"
    assert tasks[-1].name == "T150"
    assert all(isinstance(t, Task) for t in tasks)


def test_list_tasks_large_db_offset_and_limit(make_tasks, test_session):
    make_tasks(150)
    tasks = list_tasks(test_session, offset=30, limit=50)
    assert len(tasks) == 50
    assert tasks[0].name == "T31"
    assert tasks[1].name == "T32"
    assert tasks[-1].name == "T80"
    assert all(isinstance(t, Task) for t in tasks)


def test_list_tasks_large_db_limit(make_tasks, test_session):
    make_tasks(150)
    tasks = list_tasks(test_session, offset=0, limit=75)
    assert len(tasks) == 75
    assert tasks[0].name == "T1"
    assert tasks[1].name == "T2"
    assert tasks[-1].name == "T75"
    assert all(isinstance(t, Task) for t in tasks)


def test_list_tasks_large_offset_near_end(make_tasks, test_session):
    make_tasks(150)
    tasks = list_tasks(test_session, offset=145, limit=100)
    assert len(tasks) == 5
    assert tasks[0].name == "T146"
    assert tasks[1].name == "T147"
    assert tasks[-1].name == "T150"
    assert all(isinstance(t, Task) for t in tasks)


def test_list_tasks_large_db_offset_beyond_length(make_tasks, test_session):
    make_tasks(150)

    tasks = list_tasks(test_session, offset=150, limit=10)
    assert tasks == []


def test_list_tasks_large_db_zero_limit(make_tasks, test_session):
    make_tasks(150)

    tasks = list_tasks(test_session, offset=0, limit=0)
    assert tasks == []


def test_list_tasks_large_db_large_limit(make_tasks, test_session):
    make_tasks(150)
    tasks = list_tasks(test_session, offset=0, limit=999)
    assert len(tasks) == 150
    assert tasks[0].name == "T1"
    assert tasks[1].name == "T2"
    assert tasks[-1].name == "T150"
    assert all(isinstance(t, Task) for t in tasks)


## Tests for get_task


def test_get_task_valid_id(make_tasks, test_session):
    make_tasks(5)
    task = get_task(test_session, 3)
    assert isinstance(task, Task)
    assert task.name == "T3"
    assert task.priority is None
    assert task.complete is False
    assert task.project_id is None


def test_get_task_invalid_id(make_tasks, test_session):
    make_tasks(5)
    task = get_task(test_session, 6)
    assert task is None


## Tests for create_task


def test_create_task(make_tasks, test_session):
    make_tasks(5)
    task_create = TaskCreate(name="test task", priority=3)
    db_task = create_task(test_session, task_create)
    assert isinstance(db_task, Task)
    assert db_task.id is not None
    assert db_task.name == "test task"
    assert db_task.priority == 3
    assert db_task.complete is False
    assert db_task.project_id is None

    fetched = test_session.get(Task, db_task.id)
    assert fetched is not None
    assert fetched.name == "test task"


## Tests for delete_task


def test_delete_task_valid(make_tasks, test_session):
    make_tasks(5)
    success = delete_task(test_session, 3)

    assert success is True
    tasks = test_session.exec(select(Task)).all()
    assert len(tasks) == 4
    assert test_session.get(Task, 3) is None
    assert test_session.get(Task, 5) is not None


def test_delete_task_invalid(make_tasks, test_session):
    make_tasks(5)
    success = delete_task(test_session, 6)
    tasks = test_session.exec(select(Task)).all()
    assert success is False
    assert len(tasks) == 5


def test_update_task_valid(make_tasks, test_session):
    make_tasks(5)
    task_update = TaskUpdate(name="Buy milk", priority=3, complete=True)
    result = update_task(test_session, 2, task_update)
    assert isinstance(result, Task)
    assert result.name == "Buy milk"
    assert result.priority == 3
    assert result.complete is True


def test_update_task_invalid_task(make_tasks, test_session):
    make_tasks(5)
    task_update = TaskUpdate(name="Tidy house", priority=2, complete=True)
    result = update_task(test_session, 6, task_update)
    assert result is None
    tasks = test_session.exec(select(Task)).all()
    assert all(t.name != "Tidy house" for t in tasks)
