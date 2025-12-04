"""Main Textual application class."""

from textual.app import App
from textual.binding import Binding

from .database.db_manager import db_manager
from .services.project_service import project_service
from .services.tracking_service import tracking_service
from .ui.screens.main_screen import MainScreen
from .ui.screens.summary_screen import SummaryScreen
from .ui.screens.detail_screen import DetailScreen
from .utils.constants import DB_PATH


class TimeTrackerApp(App):
    """Time tracking TUI application."""

    CSS_PATH = "styles.css"

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
    ]

    def __init__(self, **kwargs):
        """Initialize the application."""
        super().__init__(**kwargs)
        self.projects = []
        self.active_entry = None

    def on_mount(self) -> None:
        """Handle application mount."""
        # Initialize database
        db_manager.initialize(DB_PATH)

        # Load projects
        self.projects = project_service.load_projects()

        # Check for active tracking
        self.active_entry = tracking_service.get_current_status()

        # Show main screen
        self.push_screen(MainScreen())

    def action_show_main(self) -> None:
        """Show the main tracking screen."""
        self.push_screen(MainScreen())

    def action_show_summary(self) -> None:
        """Show the summary report screen."""
        self.push_screen(SummaryScreen())

    def action_show_detail(self) -> None:
        """Show the detail report screen."""
        self.push_screen(DetailScreen())
