"""Service for managing projects."""

from pathlib import Path
from typing import List

from ..utils.constants import PROJECTS_FILE


class ProjectService:
    """Handle project management operations."""

    def __init__(self, projects_file: Path = PROJECTS_FILE):
        """
        Initialize the project service.

        Args:
            projects_file: Path to the projects.txt file
        """
        self.projects_file = projects_file

    def load_projects(self) -> List[str]:
        """
        Load projects from the projects.txt file.

        Creates the file with a default project if it doesn't exist.
        Returns at least one project.

        Returns:
            List of project names
        """
        # Ensure data directory exists
        self.projects_file.parent.mkdir(parents=True, exist_ok=True)

        # Create file with default project if it doesn't exist
        if not self.projects_file.exists():
            self.projects_file.write_text("Default Project\n")

        # Read and parse projects
        content = self.projects_file.read_text()
        projects = [
            line.strip()
            for line in content.splitlines()
            if line.strip()  # Filter out empty lines
        ]

        # Ensure at least one project exists
        if not projects:
            projects = ["Default Project"]
            self.projects_file.write_text("Default Project\n")

        return projects

    def is_valid_project(self, project_name: str, projects: List[str]) -> bool:
        """
        Check if a project name is valid.

        Args:
            project_name: Name to validate
            projects: List of valid project names

        Returns:
            True if valid, False otherwise
        """
        return project_name.strip() in projects


# Global service instance
project_service = ProjectService()
