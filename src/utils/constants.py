"""Application-wide constants."""

from pathlib import Path

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# File paths
DB_PATH = DATA_DIR / "timetracker.db"
PROJECTS_FILE = DATA_DIR / "projects.txt"

# UI update intervals
UPDATE_INTERVAL = 1.0  # seconds
