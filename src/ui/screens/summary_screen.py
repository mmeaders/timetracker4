"""Summary report screen."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Header, Static

from ...services.tracking_service import tracking_service
from ...utils.time_utils import format_elapsed_time


class SummaryScreen(Screen):
    """Summary report showing total time per project."""

    BINDINGS = [
        Binding("m", "pop_screen", "Main"),
        Binding("d", "show_detail", "Detail"),
        Binding("escape", "pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the summary screen layout."""
        yield Header()
        yield Container(
            Vertical(
                Static("Summary Report", id="report-title"),
                DataTable(id="summary-table"),
                Container(
                    Button("Main", id="main-btn", variant="primary"),
                    Button("Detail", id="detail-btn"),
                    id="button-container"
                ),
                id="summary-container"
            )
        )

    def on_mount(self) -> None:
        """Handle screen mount."""
        # Set up the data table
        table = self.query_one("#summary-table", DataTable)
        table.add_columns("Project", "Total Time")
        table.cursor_type = "row"

        # Load summary data
        self.load_summary_data()

    def load_summary_data(self) -> None:
        """Load and display summary data."""
        table = self.query_one("#summary-table", DataTable)
        table.clear()

        # Get summary report
        totals = tracking_service.get_summary_report()

        # Sort by total time (descending)
        sorted_projects = sorted(
            totals.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Add rows
        grand_total = 0
        for project, total_seconds in sorted_projects:
            table.add_row(project, format_elapsed_time(total_seconds))
            grand_total += total_seconds

        # Add separator and total
        if sorted_projects:
            table.add_row("─" * 20, "─" * 15)
            table.add_row("[bold]TOTAL[/bold]", f"[bold]{format_elapsed_time(grand_total)}[/bold]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "main-btn":
            self.app.pop_screen()
        elif event.button.id == "detail-btn":
            self.action_show_detail()

    def action_show_detail(self) -> None:
        """Show the detail screen."""
        from .detail_screen import DetailScreen
        self.app.push_screen(DetailScreen())
