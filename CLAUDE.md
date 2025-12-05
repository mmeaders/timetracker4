# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
TimeTracker4 is a compact TUI (Terminal User Interface) time-tracking application built with Python and Textual. It's designed to be calculator-sized in the terminal with persistent tracking that survives app restarts.

## Development Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the application:**
```bash
python -m src.main
```

**Manual testing:**
No automated test suite exists. Test by running the app and exercising the UI. Verify database state with:
```bash
sqlite3 data/timetracker.db "SELECT * FROM timeTracking;"
sqlite3 data/timetracker.db "SELECT * FROM transactions;"
```

## Architecture

### Layered Architecture
```
UI Layer (src/ui/screens/)
    ↓ calls
Service Layer (src/services/)
    ↓ calls
Repository Layer (src/database/*_repo.py)
    ↓ queries
Database Layer (db_manager.py → SQLite)
```

**Key principle:** UI screens communicate with services, not directly with the database. Services orchestrate business logic and call repositories for data access.

### Design Patterns

1. **Singleton Pattern**: All services and repositories expose module-level singleton instances:
   ```python
   from src.services.tracking_service import tracking_service  # Use this instance
   from src.services.project_service import project_service    # Use this instance
   ```

2. **Repository Pattern**: Data access is abstracted in dedicated repository classes (`tracking_repo`, `transaction_repo`)

3. **Service Return Pattern**: Services return tuples for operations:
   ```python
   (success: bool, message: str, entry: TrackingEntry)
   ```

## Key Conventions

### Time Representation
- **Timestamps**: Unix timestamps (`int(time.time())`) stored as integers
- **Durations**: Seconds (integer)
- Database columns follow this pattern consistently

### Single Active Session Rule
- Only one project can be tracked at a time
- Check via `tracking_repo.get_active_entry()` (returns entry with `stopTime=NULL`)
- Enforce this constraint in `tracking_service.start_tracking()`

### Persistent Tracking
- Active sessions (stopTime=NULL) survive app crashes/restarts
- The database is the source of truth for active state
- UI queries `tracking_service.get_current_status()` at startup to resume

### Transactions
- All start/stop events are logged in the `transactions` table as audit trail
- Actions stored as strings: `'Start'` or `'Stop'`
- Inserted via `transaction_repo.insert_transaction(...)`

## Critical Files

| File | Purpose |
|------|---------|
| [src/main.py](src/main.py) | Entry point - instantiates and runs `TimeTrackerApp` |
| [src/app.py](src/app.py) | Top-level Textual app - initialization, screen routing |
| [src/services/tracking_service.py](src/services/tracking_service.py) | Core business logic for start/stop/reports |
| [src/services/project_service.py](src/services/project_service.py) | Project management (loads from `data/projects.txt`) |
| [src/database/db_manager.py](src/database/db_manager.py) | SQLite connection singleton + transaction context manager |
| [src/database/schema.py](src/database/schema.py) | DDL statements for database tables |
| [src/database/tracking_repo.py](src/database/tracking_repo.py) | CRUD operations for `timeTracking` table |
| [src/database/transaction_repo.py](src/database/transaction_repo.py) | CRUD operations for `transactions` table |
| [src/models/tracking_entry.py](src/models/tracking_entry.py) | `TrackingEntry` dataclass with `calculate_current_elapsed()` helper |
| [src/ui/screens/main_screen.py](src/ui/screens/main_screen.py) | Primary UI - start/stop button, live elapsed time display |
| [src/utils/constants.py](src/utils/constants.py) | Path constants (`DB_PATH`, `PROJECTS_FILE`, etc.) |
| [src/utils/time_utils.py](src/utils/time_utils.py) | Time formatting utilities |

## Database Schema

**transactions** (audit log):
- `transactionId` - Sequential ID
- `action` - 'Start' or 'Stop'
- `timeStamp` - Unix timestamp (integer)
- `projectName` - Project name (text)

**timeTracking** (session records):
- `entryId` - Sequential ID
- `projectName` - Project name (text)
- `startTime` - Unix timestamp (integer)
- `stopTime` - Unix timestamp (integer, NULL if active)
- `timeElapsed` - Duration in seconds (integer, NULL if active)

**Active session indicator**: `stopTime IS NULL` in `timeTracking` table

## Data Files

| File | Purpose |
|------|---------|
| `data/projects.txt` | Project list (one per line, plain text) |
| `data/timetracker.db` | SQLite database |

Both created automatically on first run if missing.

## Common Modification Points

**Change UI behavior:**
- Modify screens in [src/ui/screens/](src/ui/screens/)
- Keyboard shortcuts defined via `on_key()` methods
- Current shortcuts: `s` (start/stop), `r` (reports), `q` (quit), `m` (main), `d` (detail)

**Change business logic:**
- Modify services in [src/services/](src/services/)
- Keep database access in repositories, not in services

**Schema changes:**
- Update DDL in [src/database/schema.py](src/database/schema.py)
- **No migration framework exists** - manually handle existing databases
- Document migration steps in README or commit message

**Add new UI screen:**
1. Create screen class in [src/ui/screens/](src/ui/screens/)
2. Add screen installation in [src/app.py](src/app.py) `on_mount()`
3. Add navigation via `app.push_screen()` or `app.switch_screen()`

## Important Notes

- **No automated tests**: Rely on manual testing via `python -m src.main`
- **Use singleton instances**: Import services/repos as module-level instances, don't create new ones
- **Database access**: Use `db_manager.transaction()` context manager for raw SQL if needed
- **Textual reactive properties**: UI automatically updates when `@reactive` properties change
- **Project loading**: Projects are loaded once at app startup from `data/projects.txt` into `app.projects`
