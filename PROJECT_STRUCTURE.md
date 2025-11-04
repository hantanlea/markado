
# Project Structure Overview

This file explains what each folder and file in the repo is for.

---

## Root (`todo-list/`)

| Path | Description |
|------|--------------|
| **backend/** | The Python backend project (FastAPI + SQLModel + Alembic). |
| **frontend/** | Placeholder for the future React app. |
| **COMMIT_CONVENTIONS.md** | Explains how to write commit messages (Conventional Commits). |
| **PROJECT_STRUCTURE.md** | This document — overview of the repo layout. |
| **.pre-commit-config.yaml** | Configuration for Git pre-commit hooks (linting, mypy, commit message checks). |
| **.gitignore** | Tells Git which files/folders to ignore (like `.venv/`, `__pycache__/`, `.env`, etc.). |

---

## Backend (`backend/`)

| Path | Description |
|------|--------------|
| **pyproject.toml** | Project configuration — dependencies, dev tools (Ruff, mypy, pytest). |
| **uv.lock** | Auto-generated lock file (exact dependency versions). Commit this! |
| **alembic.ini** | Alembic config file (base settings for database migrations). |
| **README.md** | Optional: backend-specific notes (you can add one). |
| **migrations/** | Folder managed by Alembic — stores database migration scripts. |
| **migrations/env.py** | Alembic’s environment file — connects migrations to your models and DB URL. |
| **migrations/versions/** | Auto-generated migration files (each one represents a schema change). |
| **src/** | All backend source code lives here (so imports behave the same everywhere). |

---

## Backend source (`backend/src/todo_backend/`)

| File | Description |
|------|--------------|
| **\_\_init\_\_.py** | Marks this folder as a Python package (`todo_backend`). |
| **app.py** | FastAPI app entry point — defines your API and endpoints. |
| **database.py** | Database setup — creates the SQLModel engine, connects Alembic, etc. |
| **models.py** | SQLModel classes (your database tables). |
| **\_\_pycache\_\_/** | Python’s compiled bytecode cache — ignored by Git. |

---

## Future frontend (`frontend/`)
This will hold your React (or other) frontend code — e.g. a Vite or Next.js app.  
It’s separate so Node/npm dependencies don’t interfere with the backend Python environment.

---

## Virtual environments

- **backend/.venv/** — local Python virtual environment for backend.  
  - Keeps dependencies isolated.  
  - Do **not** commit this folder.  
  - GitHub Actions / CI will recreate it automatically from `pyproject.toml` and `uv.lock`.

---

## Database & environment files

| File | Description |
|------|--------------|
| **backend/.env** | Local environment variables (DB URL, secrets, etc.). Not committed. |
| **backend/.env.example** | Template for `.env` — safe to commit. |
| **backend/dev.db** | SQLite dev database (ignored by Git). Created automatically. |

---

## Pre-commit tools

Your pre-commit setup runs automatically before each commit:
- **Ruff** → lints and formats code
- **Mypy** → enforces type hints
- **Conventional Commit hook** → checks commit message format

To run them manually:
```bash
pre-commit run --all-files

