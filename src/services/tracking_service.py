"""Service for tracking time on projects."""

import time
from typing import Dict, List, Optional, Tuple

from ..database.tracking_repo import tracking_repo
from ..database.transaction_repo import transaction_repo
from ..models.tracking_entry import TrackingEntry


class TrackingService:
    """Handle business logic for time tracking operations."""

    def start_tracking(self, project_name: str) -> Tuple[bool, str, Optional[TrackingEntry]]:
        """
        Start tracking time for a project.

        Args:
            project_name: Name of the project to track

        Returns:
            Tuple of (success, message, tracking_entry)
            - success: True if started successfully
            - message: Status or error message
            - tracking_entry: Created entry if successful, None otherwise
        """
        # Check if there's already an active tracking session
        active_entry = tracking_repo.get_active_entry()

        if active_entry is not None:
            return (
                False,
                f"Already tracking '{active_entry.project_name}'. Stop it first.",
                None
            )

        # Start tracking
        current_time = int(time.time())

        # Create transaction record
        transaction_repo.insert_transaction('Start', current_time, project_name)

        # Create tracking entry
        entry_id = tracking_repo.insert_tracking_entry(project_name, current_time)

        # Retrieve and return the created entry
        entry = tracking_repo.get_entry_by_id(entry_id)

        return (
            True,
            f"Started tracking '{project_name}'",
            entry
        )

    def stop_tracking(self) -> Tuple[bool, str, Optional[TrackingEntry]]:
        """
        Stop the currently active tracking session.

        Returns:
            Tuple of (success, message, tracking_entry)
            - success: True if stopped successfully
            - message: Status or error message
            - tracking_entry: Updated entry if successful, None otherwise
        """
        # Get active entry
        active_entry = tracking_repo.get_active_entry()

        if active_entry is None:
            return (
                False,
                "No active tracking session to stop.",
                None
            )

        # Stop tracking
        current_time = int(time.time())
        elapsed = current_time - active_entry.start_time

        # Create Stop transaction
        transaction_repo.insert_transaction('Stop', current_time, active_entry.project_name)

        # Update tracking entry
        tracking_repo.update_tracking_entry(
            active_entry.entry_id,
            current_time,
            elapsed
        )

        # Retrieve updated entry
        entry = tracking_repo.get_entry_by_id(active_entry.entry_id)

        return (
            True,
            f"Stopped tracking '{active_entry.project_name}'",
            entry
        )

    def get_current_status(self) -> Optional[TrackingEntry]:
        """
        Get the current tracking status.

        Returns:
            Active TrackingEntry if tracking, None otherwise
        """
        return tracking_repo.get_active_entry()

    def get_summary_report(self) -> Dict[str, int]:
        """
        Get summary report of total time per project.

        Returns:
            Dictionary mapping project name to total seconds
        """
        totals = tracking_repo.get_project_totals()

        # Also include time from active session if any
        active_entry = tracking_repo.get_active_entry()
        if active_entry:
            current_elapsed = active_entry.calculate_current_elapsed()
            project = active_entry.project_name

            if project in totals:
                totals[project] += current_elapsed
            else:
                totals[project] = current_elapsed

        return totals

    def get_detail_report(self, project_name: Optional[str] = None) -> List[TrackingEntry]:
        """
        Get detailed report of tracking sessions.

        Args:
            project_name: Optional project name to filter by

        Returns:
            List of TrackingEntry objects
        """
        if project_name:
            return tracking_repo.get_entries_by_project(project_name)
        else:
            return tracking_repo.get_all_entries()


# Global service instance
tracking_service = TrackingService()
