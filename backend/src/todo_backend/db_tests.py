from sqlmodel import Session, select

from todo_backend.database import engine
from todo_backend.models import Project, Task


def create_tasks() -> None:
    with Session(engine) as session:
        project_coding = Project(name="Coding")
        project_french = Project(name="French")
        project_selfbuild = Project(name="Selfbuild")

        task1 = Task(name="Listen to French podcast", project=project_french)
        task2 = Task(name="Learn sqlmodel", project=project_coding)
        task3 = Task(name="Look at eco homes", project=project_selfbuild)

        session.add(task1)
        session.add(task2)
        session.add(task3)
        session.commit()


def select_tasks():
    with Session(engine) as session:
        statement = select(Task).where(Task.name == "Learn sqlmodel")
        result = session.exec(statement)
        task_one = result.one()
        print(task_one.project)
