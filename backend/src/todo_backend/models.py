from sqlmodel import Field, Relationship, SQLModel

# PROJECT CLASSES


class ProjectBase(SQLModel):
    name: str = Field(index=True)


class Project(ProjectBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tasks: list["Task"] = Relationship(back_populates="project")


class ProjectCreate(ProjectBase):
    tasks: list["Task"]


class ProjectPublic(ProjectBase):
    id: int
    tasks: list["Task"]


# TASK CLASSES


class TaskBase(SQLModel):
    name: str = Field(index=True)
    priority: int | None = Field(default=None)
    # context: str | None = Field(default=None)
    complete: bool = Field(default=False)
    project_id: int | None = Field(default=None, foreign_key="project.id")


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project: Project | None = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class TaskPublic(TaskBase):
    id: int
