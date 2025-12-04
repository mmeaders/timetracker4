"""Repository for timeTracking table operations."""

from typing import Dict, List, Optional

from ..models.tracking_entry import TrackingEntry
from .db_manager import db_manager


class TrackingRepository:
    """Handle database operations for the timeTracking table."""

    def insert_tracking_entry(self, project_name: str, start_time: int) -> int:
        """
        Insert a new tracking entry (started but not stopped).

        Args:
            project_name: Name of the project
            start_time: Unix timestamp when tracking started

        Returns:
            Entry ID of the inserted record
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO timeTracking (projectName, startTime, stopTime, timeElapsed)
            VALUES (?, ?, NULL, NULL)
            """,
            (project_name, start_time)
        )
        conn.commit()

        return cursor.lastrowid

    def update_tracking_entry(
        self,
        entry_id: int,
        stop_time: int,
        elapsed: int
    ) -> None:
        """
        Update a tracking entry with stop time and elapsed duration.

        Args:
            entry_id: Entry ID to update
            stop_time: Unix timestamp when tracking stopped
            elapsed: Total elapsed time in seconds
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE timeTracking
            SET stopTime = ?, timeElapsed = ?
            WHERE entryId = ?
            """,
            (stop_time, elapsed, entry_id)
        )
        conn.commit()

    def get_active_entry(self) -> Optional[TrackingEntry]:
        """
        Get the currently active tracking entry (if any).

        Returns:
            TrackingEntry object or None if no active tracking
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT entryId, projectName, startTime, stopTime, timeElapsed
            FROM timeTracking
            WHERE stopTime IS NULL
            LIMIT 1
            """
        )

        row = cursor.fetchone()
        if row:
            return TrackingEntry(
                entry_id=row['entryId'],
                project_name=row['projectName'],
                start_time=row['startTime'],
                stop_time=row['stopTime'],
                time_elapsed=row['timeElapsed']
            )
        return None

    def get_entry_by_id(self, entry_id: int) -> Optional[TrackingEntry]:
        """
        Get a tracking entry by its ID.

        Args:
            entry_id: Entry ID to retrieve

        Returns:
            TrackingEntry object or None if not found
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT entryId, projectName, startTime, stopTime, timeElapsed
            FROM timeTracking
            WHERE entryId = ?
            """,
            (entry_id,)
        )

        row = cursor.fetchone()
        if row:
            return TrackingEntry(
                entry_id=row['entryId'],
                project_name=row['projectName'],
                start_time=row['startTime'],
                stop_time=row['stopTime'],
                time_elapsed=row['timeElapsed']
            )
        return None

    def get_entries_by_project(self, project_name: str) -> List[TrackingEntry]:
        """
        Get all tracking entries for a specific project.

        Args:
            project_name: Name of the project

        Returns:
            List of TrackingEntry objects
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT entryId, projectName, startTime, stopTime, timeElapsed
            FROM timeTracking
            WHERE projectName = ?
            ORDER BY startTime DESC
            """,
            (project_name,)
        )

        rows = cursor.fetchall()
        return [
            TrackingEntry(
                entry_id=row['entryId'],
                project_name=row['projectName'],
                start_time=row['startTime'],
                stop_time=row['stopTime'],
                time_elapsed=row['timeElapsed']
            )
            for row in rows
        ]

    def get_all_entries(self, completed_only: bool = False) -> List[TrackingEntry]:
        """
        Get all tracking entries.

        Args:
            completed_only: If True, only return completed entries

        Returns:
            List of TrackingEntry objects
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        if completed_only:
            query = """
                SELECT entryId, projectName, startTime, stopTime, timeElapsed
                FROM timeTracking
                WHERE stopTime IS NOT NULL
                ORDER BY startTime DESC
            """
        else:
            query = """
                SELECT entryId, projectName, startTime, stopTime, timeElapsed
                FROM timeTracking
                ORDER BY startTime DESC
            """

        cursor.execute(query)
        rows = cursor.fetchall()

        return [
            TrackingEntry(
                entry_id=row['entryId'],
                project_name=row['projectName'],
                start_time=row['startTime'],
                stop_time=row['stopTime'],
                time_elapsed=row['timeElapsed']
            )
            for row in rows
        ]

    def get_project_totals(self) -> Dict[str, int]:
        """
        Get total time spent on each project.

        Returns:
            Dictionary mapping project name to total seconds
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT projectName, SUM(timeElapsed) as total
            FROM timeTracking
            WHERE stopTime IS NOT NULL
            GROUP BY projectName
            """
        )

        rows = cursor.fetchall()
        return {row['projectName']: row['total'] or 0 for row in rows}


# Global repository instance
tracking_repo = TrackingRepository()
