"""Transaction model for tracking start/stop events."""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional


@dataclass
class Transaction:
    """Represents a single start or stop transaction."""

    transaction_id: Optional[int]
    action: Literal['Start', 'Stop']
    timestamp: int  # Unix timestamp (seconds since epoch)
    project_name: str

    @property
    def datetime(self) -> datetime:
        """Convert Unix timestamp to datetime object."""
        return datetime.fromtimestamp(self.timestamp)

    @property
    def formatted_datetime(self) -> str:
        """Return formatted datetime string."""
        return self.datetime.strftime('%Y-%m-%d %H:%M:%S')
