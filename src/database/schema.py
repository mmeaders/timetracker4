"""Database schema definitions for the time tracking application."""

CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions (
    transactionId INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL CHECK(action IN ('Start', 'Stop')),
    timeStamp INTEGER NOT NULL,
    projectName TEXT NOT NULL
);
"""

CREATE_TRANSACTIONS_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_transactions_project
    ON transactions(projectName);

CREATE INDEX IF NOT EXISTS idx_transactions_timestamp
    ON transactions(timeStamp DESC);
"""

CREATE_TIMETRACKING_TABLE = """
CREATE TABLE IF NOT EXISTS timeTracking (
    entryId INTEGER PRIMARY KEY AUTOINCREMENT,
    projectName TEXT NOT NULL,
    startTime INTEGER NOT NULL,
    stopTime INTEGER,
    timeElapsed INTEGER,
    CHECK(stopTime IS NULL OR stopTime >= startTime)
);
"""

CREATE_TIMETRACKING_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_timetracking_project
    ON timeTracking(projectName);

CREATE INDEX IF NOT EXISTS idx_timetracking_active
    ON timeTracking(stopTime) WHERE stopTime IS NULL;
"""


def get_schema_statements():
    """Return all schema creation statements in order."""
    return [
        CREATE_TRANSACTIONS_TABLE,
        CREATE_TRANSACTIONS_INDEXES,
        CREATE_TIMETRACKING_TABLE,
        CREATE_TIMETRACKING_INDEXES,
    ]
