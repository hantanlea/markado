from sqlmodel import Field, Relationship, SQLModel


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    tasks: list["Task"] = Relationship(back_populates="project")


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    priority: int | None
    context: str | None
    complete: bool
    project_id: int | None = Field(default=None, foreign_key="project.id")
    project: Project | None = Relationship(back_populates="tasks")
