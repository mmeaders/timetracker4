"""Repository for transaction table operations."""

from typing import List, Literal, Optional

from ..models.transaction import Transaction
from .db_manager import db_manager


class TransactionRepository:
    """Handle database operations for the transactions table."""

    def insert_transaction(
        self,
        action: Literal['Start', 'Stop'],
        timestamp: int,
        project_name: str
    ) -> int:
        """
        Insert a new transaction record.

        Args:
            action: 'Start' or 'Stop'
            timestamp: Unix timestamp
            project_name: Name of the project

        Returns:
            Transaction ID of the inserted record
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO transactions (action, timeStamp, projectName)
            VALUES (?, ?, ?)
            """,
            (action, timestamp, project_name)
        )
        conn.commit()

        return cursor.lastrowid

    def get_transactions_by_project(self, project_name: str) -> List[Transaction]:
        """
        Get all transactions for a specific project.

        Args:
            project_name: Name of the project

        Returns:
            List of Transaction objects
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT transactionId, action, timeStamp, projectName
            FROM transactions
            WHERE projectName = ?
            ORDER BY timeStamp DESC
            """,
            (project_name,)
        )

        rows = cursor.fetchall()
        return [
            Transaction(
                transaction_id=row['transactionId'],
                action=row['action'],
                timestamp=row['timeStamp'],
                project_name=row['projectName']
            )
            for row in rows
        ]

    def get_recent_transactions(self, limit: int = 50) -> List[Transaction]:
        """
        Get recent transactions across all projects.

        Args:
            limit: Maximum number of transactions to return

        Returns:
            List of Transaction objects
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT transactionId, action, timeStamp, projectName
            FROM transactions
            ORDER BY timeStamp DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()
        return [
            Transaction(
                transaction_id=row['transactionId'],
                action=row['action'],
                timestamp=row['timeStamp'],
                project_name=row['projectName']
            )
            for row in rows
        ]

    def get_last_transaction_for_project(
        self,
        project_name: str
    ) -> Optional[Transaction]:
        """
        Get the most recent transaction for a project.

        Args:
            project_name: Name of the project

        Returns:
            Transaction object or None if no transactions exist
        """
        conn = db_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT transactionId, action, timeStamp, projectName
            FROM transactions
            WHERE projectName = ?
            ORDER BY timeStamp DESC
            LIMIT 1
            """,
            (project_name,)
        )

        row = cursor.fetchone()
        if row:
            return Transaction(
                transaction_id=row['transactionId'],
                action=row['action'],
                timestamp=row['timeStamp'],
                project_name=row['projectName']
            )
        return None


# Global repository instance
transaction_repo = TransactionRepository()
