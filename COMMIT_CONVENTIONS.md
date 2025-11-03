# Commit Message Conventions

This project follows the **Conventional Commits** standard.

Each commit message should start with a **type**, an optional **scope**, and a short **description**:
<type>(<scope>): <description>

---

## Types

| Type | Purpose |
|------|----------|
| **feat** | A new feature for the user or API |
| **fix** | A bug fix |
| **chore** | Routine maintenance or tooling (no production code changes) |
| **docs** | Documentation only |
| **test** | Adding or updating tests |
| **refactor** | Code change that neither fixes a bug nor adds a feature |
| **style** | Formatting, linting, or stylistic changes (no logic changes) |
| **perf** | Performance improvements |
| **build** | Changes to build tools, dependencies, or packaging |
| **ci** | Continuous Integration / deployment configuration changes |

---

## Examples
feat(todo): add endpoint to create new todos
fix(db): correct SQLite connection string
chore(backend): add .env and dotenv support
docs: explain project folder structure
test(api): add health route test
refactor(models): simplify user schema
style: apply Ruff auto-fixes

---

## Rules

- Use the **imperative mood** (“add feature”, not “added feature”).
- Keep descriptions short (≤ 72 characters).
- Reference an issue or PR if relevant (`fix: resolve #12`).
- Include a **scope** in parentheses if the change affects a specific area (`feat(api): ...`, `fix(db): ...`).
- Commits should represent *one logical change* — don’t mix unrelated edits.

---

## Why It Matters

- Makes commit history easy to scan and understand.
- Enables automatic changelog generation.
- Helps semantic versioning tools detect new features and fixes.
- Keeps project history consistent and professional.

---

**Further reading:**  
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
