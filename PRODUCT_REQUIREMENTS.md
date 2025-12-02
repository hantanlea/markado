# Markado Requirements

Markado is **not** a generic todo app.  
It is a pretty, integrated front-end to **markdown-based task lists**, compatible with Obsidian’s “everything is a file” philosophy.

- **Single source of truth:** markdown files in a vault.
- **Database:** used only as an index/cache for fast querying.
- **If Markado dies:** your todos still exist as plain text in your vault.

---

## Versions Overview

- **v0.1 – Backend API MVP**
  - CRUD over tasks/projects in SQLite via SQLModel.
  - Clean, tested FastAPI service.
- **v0.2 – Markdown-First Engine**
  - Markdown becomes canonical store.
  - SQLite is a derived index over markdown files.
  - Obsidian Tasks + Dataview-compatible task syntax.

Later versions (calendar, email, voice capture, mobile app) are out of scope here.

---

## v0.1 – Backend API MVP

### Scope

A small but solid backend service that:

- Runs as a FastAPI app.
- Stores tasks (and optionally projects) in SQLite via SQLModel.
- Exposes basic CRUD endpoints.
- Has tests and minimal tooling so it’s not a mess.

### Functional Requirements

#### 1. Data Model

- [ ] `Task` model
  - Fields: `id`, `name`, `priority`, `complete`, `project_id`.
  - SQLModel `TaskBase`, `Task`, `TaskCreate`, `TaskUpdate`, `TaskPublic`.
- [ ] `Project` model
  - Fields: `id`, `name`.
  - Relationship: `Project` ↔ `Task` (one-to-many).
  - SQLModel `ProjectBase`, `Project`, `ProjectCreate`, `ProjectPublic`.

#### 2. Persistence

- [ ] SQLite database using SQLModel engine.
- [ ] `DATABASE_PATH` configurable via `.env`.
- [ ] `init_db()`:
  - Verifies DB connection on startup.
  - Logs DB URL and path.
- [ ] `create_db_and_tables()`:
  - Creates tables from SQLModel metadata.
  - Only used in dev (no runtime table creation in prod).
- [ ] Alembic wired for migrations:
  - Initial migration that creates `tasks` and `projects` tables.
  - Command docs in README (`alembic revision`, `alembic upgrade`).

#### 3. API Endpoints

- [ ] `GET /health`
  - Returns `{ "status": "ok" }`.
- [ ] `GET /tasks/`
  - Pagination: `offset`, `limit` (max 100).
  - Returns list of `TaskPublic`.
- [ ] `GET /tasks/{task_id}`
  - 200 with `TaskPublic` if found.
  - 404 if not found.
- [ ] `POST /tasks/`
  - Accepts `TaskCreate`.
  - Returns created `TaskPublic`.
- [ ] `PATCH /tasks/{task_id}`
  - Accepts `TaskUpdate` (partial).
  - Returns updated `TaskPublic`.
  - 404 if not found.
- [ ] `DELETE /tasks/{task_id}`
  - Returns 204 on success.
  - 404 if not found.
- [ ] Project endpoints (basic):
  - `GET /projects/`
  - `GET /projects/{project_id}`
  - `POST /projects/`
  - Optional: `GET /projects/{project_id}/tasks`.

#### 4. Logging

- [ ] Central logging setup using `logging.config.dictConfig`.
- [ ] Logs to:
  - stderr (INFO+)
  - rotating file under configurable `LOG_DIR`.
- [ ] Logs at startup:
  - environment info (e.g. `PP_ENV`, port).
  - DB connection success/failure.

#### 5. Testing & Quality

- [ ] Unit tests for service layer:
  - `list_tasks`, `get_task`, `create_task`, `update_task`, `delete_task`.
  - Use in-memory SQLite for isolation.
- [ ] API tests using FastAPI `TestClient`:
  - Happy paths and basic error cases for all endpoints.
- [ ] `pytest` configured (via `pyproject.toml`).
- [ ] Linting + type checking:
  - `ruff` for linting/formatting.
  - `mypy` for static typing.
- [ ] Pre-commit hooks:
  - Run ruff, mypy, and pytest (or at least lint + type) before commit.

#### 6. Dev Experience / Ops

- [ ] `README.md` with:
  - How to install deps (uv).
  - How to run the app (uvicorn command).
  - How to run tests.
  - How to run migrations.
- [ ] Example `.env.example` with:
  - `DATABASE_PATH`
  - `LOG_DIR`
  - `LOG_LEVEL`
- [ ] Optional: simple Makefile/justfile targets:
  - `run`, `test`, `lint`, `type`, `migrate`.

### Non-Goals for v0.1

- No authentication / multi-user.
- No markdown parsing.
- No mobile or web UI.
- No syncing between devices (beyond what SQLite gives you locally).

---

## v0.2 – Markdown-First Engine

### Scope

Transition from “tasks live in the DB” to:

> **Markdown files are the single source of truth**  
> SQLite exists only as an index derived from those files.

The API should still feel similar to v0.1 for clients, but under the hood, every change goes through the markdown layer.

### Functional Requirements

#### 1. Markdown Task Specification

- [ ] Define supported task syntaxes:
  - Obsidian Tasks plugin style:
    - `- [ ] Task text`
    - Optional inline metadata (emoji, tags).
  - Dataview inline fields:
    - `key:: value` pairs on the same line as the task.
  - YAML frontmatter:
    - Optional file-level metadata that applies to tasks.
- [ ] Decide on canonical mapping to internal Task fields:
  - `name` (task text)
  - `complete`
  - `due`
  - `priority`
  - `tags`
  - `project` / file-based context

#### 2. Vault Layout

- [ ] Configuration for vault root: `VAULT_DIR`.
- [ ] Decide and document:
  - Which folders/files are scanned for tasks.
  - Whether “projects” are:
    - per-file (one project per file), or
    - defined by frontmatter, or
    - defined by folder structure.

#### 3. Markdown Parser

- [ ] Implement parser that:
  - Walks vault directory tree from `VAULT_DIR`.
  - Parses each markdown file into:
    - file metadata (frontmatter, path).
    - task list: each with position (line number or block identifier).
  - Handles Tasks + Dataview syntax.
- [ ] Parser outputs a normalized internal representation:
  - `TaskIndexItem`:
    - `file_path`
    - `line_number` / `block_id`
    - `name`
    - `complete`
    - `due`
    - `priority`
    - `tags`
    - `project_id` / project label
    - timestamps where applicable.

#### 4. SQLite as Index

- [ ] Introduce an index table (or tables) to store parsed tasks:
  - `id` (internal index id)
  - `file_path`
  - `line_number` / `block_id`
  - `name`
  - `complete`
  - `due`
  - `priority`
  - `tags` (serialized list or separate table)
  - `project_ref` (however projects are represented)
- [ ] Indexer process:
  - Full scan mode:
    - Clear index and rebuild from vault.
  - Incremental mode:
    - Detect changed/added/deleted files via mtime or hash.
    - Re-parse only changed files.
    - Remove index rows for deleted files.
- [ ] Guarantee: if the index is dropped, it can be fully regenerated from markdown.

#### 5. Write Path: API → Markdown → Index

- [ ] All mutations to tasks go through this pipeline:
  - API receives request (e.g. “complete task”).
  - Lookup task in index to obtain `file_path` + `line_number` / `block_id`.
  - Load that markdown file.
  - Apply text change:
    - e.g. `- [ ]` → `- [x]`, add `completed::` field, update `due::` etc.
  - Save file to disk.
  - Re-parse the changed file and update index entries.
- [ ] If file write fails, API returns error and **does not** modify the index.

#### 6. External Changes (Obsidian, sync tools, etc.)

- [ ] Indexer must handle the case where:
  - Files are edited directly in Obsidian.
  - Files are added/removed by sync.
- [ ] Change detection:
  - At minimum: mtime check per file.
  - Optional: hash to avoid re-parsing unchanged content.
- [ ] APIs / triggers:
  - Endpoint to trigger “resync vault now”.
  - Optional periodic or on-demand incremental scan strategy.

#### 7. API Adaptations for Markdown World

- [ ] /tasks endpoints should operate on **indexed tasks**, not raw DB tasks.
- [ ] New helper endpoints:
  - `POST /resync` (or similar) to trigger reindex.
  - `GET /files/{path}` to fetch full file text (for future clients/editor UI).
  - Optional: `GET /projects/` derived from file structure/metadata rather than DB table.

#### 8. Config & Safety

- [ ] Configurable:
  - `VAULT_DIR`
  - Included/excluded folders.
- [ ] Safe defaults:
  - Never modify files outside configured vault.
  - No destructive operations on files without explicit intent.

### Non-Goals for v0.2

- No Dataview query language support (just syntax for storing metadata).
- No UI/UX work beyond basic API responses.
- No calendar/email/voice integrations yet.
- No sync conflict resolution between multiple devices (beyond “last write wins” from filesystem).

---

## Future Versions (Non-Binding Sketch)

Not part of v0.1 or v0.2, but likely roadmap items:

- Calendar integrations (Google, etc.).
- Email → task capture.
- Voice capture endpoint + mobile integration.
- Mobile app (Android first) consuming the existing API.
- Better query language (Dataview-like filters) on top of the index.

---
