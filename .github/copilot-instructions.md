<!-- Copilot / AI-agent instructions for contributors working in this repository -->
# TimeTracker4 — AI agent guidance

This project is a compact TUI time-tracker built with Python and Textual. The goal of these instructions is to get an AI coding agent immediately productive by describing the architecture, conventions, and concrete examples from the codebase.

Key points (quick):
- Entry point: run `python -m src.main` (see `src/main.py`).
- App bootstrap: `TimeTrackerApp` in `src/app.py` calls `db_manager.initialize(DB_PATH)` and loads projects via `project_service.load_projects()`.
- Data: projects list at `data/projects.txt`; SQLite DB at `data/timetracker.db` (constant in `src/utils/constants.py`).

Architecture & responsibilities:
- `src/app.py` — top-level Textual application. Responsible for initialization and switching screens.
- `src/services/` — business logic. Example: `tracking_service` exposes `start_tracking`, `stop_tracking`, `get_summary_report`, and is imported as a global instance (`tracking_service`). See `src/services/tracking_service.py` for patterns and return semantics: methods return `(success: bool, message: str, entry)` for start/stop.
- `src/database/` — persistence layer. `db_manager` is a singleton wrapper around sqlite3 (`src/database/db_manager.py`). Repos live here: `tracking_repo`, `transaction_repo` — these are the canonical data access points.
- `src/models/` — small data classes (`TrackingEntry`, etc.) that represent DB rows and provide helpers such as `calculate_current_elapsed()`.
- `src/ui/screens/` — Textual screens and widgets (e.g. `MainScreen`, `SummaryScreen`, `DetailScreen`). UI communicates with services (not directly with DB) — prefer calling `tracking_service`, `project_service`, etc.

Concrete conventions and patterns (do not deviate unless necessary):
- Singleton services: components expose a module-level instance (e.g. `tracking_service = TrackingService()`). Use these rather than creating new instances.
- Time representation: use Unix timestamps (`int(time.time())`) for start/stop; durations in seconds. Database columns follow this pattern.
- Transactions: actions are stored as `'Start'`/`'Stop'` strings via `transaction_repo.insert_transaction(...)` alongside tracking entries in `tracking_repo`.
- Single active session: code enforces only one active `TrackingEntry`. `tracking_repo.get_active_entry()` is the canonical check.
- Projects: read/managed via `project_service` and `data/projects.txt`. The UI populates `Select` widget options from `app.projects` (loaded at mount).

Common tasks & examples (copyable):
- Start the app locally:
```bash
pip install -r requirements.txt
python -m src.main
```
- Inspect active entry from code (example):
```py
from src.services.tracking_service import tracking_service
active = tracking_service.get_current_status()
if active:
    secs = active.calculate_current_elapsed()
```
- Database usage pattern: use `db_manager.transaction()` context manager when writing raw SQL.

Where to change behavior safely:
- UI text/controls: `src/ui/screens/*.py` (e.g. `MainScreen` controls start/stop button, keybindings `s` and `r`).
- Business logic: `src/services/*.py` — modify here for new rules (validation, additional fields). Keep DB access in `src/database/*`.
- Schema changes: `src/database/schema.py` provides DDL statements used by `db_manager._create_schema()`; update and ensure migrations for existing DBs.

Testing & debugging notes (discoverable in repo):
- No automated tests present — rely on manual run for verification.
- Typical debugging: run `python -m src.main` and exercise the UI. Check `data/timetracker.db` using `sqlite3` CLI or a DB browser.

Useful file references (examples to open):
- `src/app.py` — app lifecycle and screen routing.
- `src/services/tracking_service.py` — business rules for start/stop and reports.
- `src/database/db_manager.py` — connection, transaction context manager, schema initialization.
- `src/ui/screens/main_screen.py` — shows how UI queries `app.projects`, uses `tracking_service`, and updates live elapsed time.

When you patch code:
- Follow existing style (small, focused changes). Prefer changing services over UI when altering business rules.
- If modifying DB schema, update `src/database/schema.py` and add upgrade steps to README (no migration framework present).

If anything here is unclear or you want more detail (examples, common PR templates, or additional file walkthroughs), tell me which files or flows to expand and I will iterate.
