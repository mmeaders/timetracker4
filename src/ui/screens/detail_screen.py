"""Detail report screen showing session history."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Header, Label, Select, Static

from ...services.tracking_service import tracking_service
from ...utils.time_utils import format_datetime_short, format_elapsed_time


class DetailScreen(Screen):
    """Detail report showing individual tracking sessions."""

    BINDINGS = [
        Binding("m", "pop_screen", "Main"),
        Binding("s", "show_summary", "Summary"),
        Binding("escape", "pop_screen", "Back"),
    ]

    def __init__(self):
        """Initialize the detail screen."""
        super().__init__()
        self.filter_project = None

    def compose(self) -> ComposeResult:
        """Compose the detail screen layout."""
        yield Header()
        yield Container(
            Vertical(
                Static("Session History", id="detail-title"),
                Label("Filter:"),
                Select(
                    options=[("All Projects", None)],
                    id="project-filter",
                    value=None
                ),
                DataTable(id="detail-table"),
                Container(
                    Button("Main", id="main-btn", variant="primary"),
                    Button("Summary", id="summary-btn"),
                    id="button-container"
                ),
                id="detail-container"
            )
        )

    def on_mount(self) -> None:
        """Handle screen mount."""
        # Set up project filter
        app = self.app
        filter_options = [("All Projects", None)]
        filter_options.extend([(proj, proj) for proj in app.projects])

        filter_select = self.query_one("#project-filter", Select)
        filter_select.set_options(filter_options)

        # Set up the data table
        table = self.query_one("#detail-table", DataTable)
        table.add_columns("Start", "Stop", "Duration", "Project")
        table.cursor_type = "row"

        # Load detail data
        self.load_detail_data()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle filter selection change."""
        if event.select.id == "project-filter":
            self.filter_project = event.value if event.value != Select.BLANK else None
            self.load_detail_data()

    def load_detail_data(self) -> None:
        """Load and display detail data."""
        table = self.query_one("#detail-table", DataTable)
        table.clear()

        # Get detail report
        entries = tracking_service.get_detail_report(self.filter_project)

        # Add rows
        for entry in entries:
            start = format_datetime_short(entry.start_time)

            if entry.is_active:
                stop = "[green]Active[/green]"
                duration = format_elapsed_time(entry.calculate_current_elapsed())
            else:
                stop = format_datetime_short(entry.stop_time)
                duration = format_elapsed_time(entry.time_elapsed)

            table.add_row(start, stop, duration, entry.project_name)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "main-btn":
            self.app.pop_screen()
        elif event.button.id == "summary-btn":
            self.action_show_summary()

    def action_show_summary(self) -> None:
        """Show the summary screen."""
        from .summary_screen import SummaryScreen
        self.app.push_screen(SummaryScreen())
