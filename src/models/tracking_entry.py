"""Tracking entry model for time tracking sessions."""

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class TrackingEntry:
    """Represents a time tracking session."""

    entry_id: Optional[int]
    project_name: str
    start_time: int  # Unix timestamp
    stop_time: Optional[int]  # None if currently running
    time_elapsed: Optional[int]  # Seconds, None if currently running

    @property
    def is_active(self) -> bool:
        """Check if this tracking session is currently active."""
        return self.stop_time is None

    def calculate_current_elapsed(self) -> int:
        """
        Calculate elapsed seconds for this entry.

        For active entries, calculates from start_time to current time.
        For completed entries, returns the stored time_elapsed.

        Returns:
            Elapsed time in seconds
        """
        if self.is_active:
            # Active entry - calculate from start to now
            current_time = int(time.time())
            return current_time - self.start_time
        else:
            # Completed entry - return stored elapsed time
            return self.time_elapsed or 0

    @property
    def start_datetime(self) -> datetime:
        """Convert start_time to datetime object."""
        return datetime.fromtimestamp(self.start_time)

    @property
    def stop_datetime(self) -> Optional[datetime]:
        """Convert stop_time to datetime object if available."""
        if self.stop_time is not None:
            return datetime.fromtimestamp(self.stop_time)
        return None

    @property
    def formatted_start(self) -> str:
        """Return formatted start datetime string."""
        return self.start_datetime.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def formatted_stop(self) -> str:
        """Return formatted stop datetime string or 'Active'."""
        if self.stop_datetime:
            return self.stop_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return 'Active'
