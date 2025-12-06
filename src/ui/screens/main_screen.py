"""Main tracking screen."""

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Select, Static, Label
from textual.reactive import reactive

from ...services.tracking_service import tracking_service
from ...utils.time_utils import format_elapsed_time


class MainScreen(Screen):
    """Main time tracking interface."""

    BINDINGS = [
        Binding("r", "show_reports", "Reports"),
        Binding("s", "toggle_tracking", "Start/Stop"),
    ]

    # Reactive attributes
    elapsed_seconds = reactive(0)
    is_tracking = reactive(False)
    current_project = reactive("")

    def __init__(self):
        """Initialize the main screen."""
        super().__init__()
        self.selected_project = None
        self.update_timer = None

    def compose(self) -> ComposeResult:
        """Compose the main screen layout."""
        yield Header()
        yield Container(
            Vertical(
                Static("Time Tracker", id="title"),
                Static("", id="status-display"),
                Static("", id="project-display"),
                Static("00:00:00", id="elapsed-display"),
                Label("Select Project:"),
                Select(
                    options=[("Loading...", "loading")],
                    id="project-select",
                    allow_blank=False
                ),
                Container(
                    Button("Start", id="start-stop-btn", variant="primary"),
                    Button("Reports", id="reports-btn"),
                    Button("Exit", id="exit-btn"),
                    id="button-container"
                ),
                id="main-container"
            )
        )

    def on_mount(self) -> None:
        """Handle screen mount."""
        # Load projects into select widget
        app = self.app
        project_options = [(proj, proj) for proj in app.projects]
        select_widget = self.query_one("#project-select", Select)
        select_widget.set_options(project_options)

        # Check for active tracking
        active_entry = app.active_entry
        if active_entry:
            self.is_tracking = True
            self.current_project = active_entry.project_name
            self.selected_project = active_entry.project_name
            select_widget.value = active_entry.project_name

            # Start live updates
            self.start_live_updates()
        else:
            self.is_tracking = False
            # Set first project as default selection
            if app.projects:
                self.selected_project = app.projects[0]
                select_widget.value = app.projects[0]

        # Update display
        self.update_display()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle project selection change."""
        if event.value != Select.BLANK:
            self.selected_project = str(event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "start-stop-btn":
            self.action_toggle_tracking()
        elif event.button.id == "reports-btn":
            self.action_show_reports()
        elif event.button.id == "exit-btn":
            self.app.exit()

    def action_toggle_tracking(self) -> None:
        """Toggle tracking on/off."""
        if self.is_tracking:
            # Stop tracking
            success, message, entry = tracking_service.stop_tracking()
            if success:
                self.is_tracking = False
                self.current_project = ""
                self.elapsed_seconds = 0
                self.stop_live_updates()
                self.app.active_entry = None
                self.notify(message)
        else:
            # Start tracking
            if not self.selected_project:
                self.notify("Please select a project first", severity="warning")
                return

            success, message, entry = tracking_service.start_tracking(self.selected_project)
            if success:
                self.is_tracking = True
                self.current_project = self.selected_project
                self.app.active_entry = entry
                self.start_live_updates()
                self.notify(message)
            else:
                # Show warning about existing tracking
                self.notify(message, severity="warning", timeout=5)

        self.update_display()

    def start_live_updates(self) -> None:
        """Start the live elapsed time updates."""
        self.update_timer = self.set_interval(1.0, self.update_elapsed_time)

    def stop_live_updates(self) -> None:
        """Stop the live elapsed time updates."""
        if self.update_timer:
            self.update_timer.stop()
            self.update_timer = None

    def update_elapsed_time(self) -> None:
        """Update the elapsed time display."""
        if self.is_tracking and self.app.active_entry:
            self.elapsed_seconds = self.app.active_entry.calculate_current_elapsed()
            elapsed_label = self.query_one("#elapsed-display", Static)
            elapsed_label.update(format_elapsed_time(self.elapsed_seconds))

    def update_display(self) -> None:
        """Update the display based on current state."""
        status_label = self.query_one("#status-display", Static)
        project_label = self.query_one("#project-display", Static)
        elapsed_label = self.query_one("#elapsed-display", Static)
        button = self.query_one("#start-stop-btn", Button)

        if self.is_tracking:
            status_label.update("Status: [green]TRACKING[/green]")
            project_label.update(f"Project: [bold]{self.current_project}[/bold]")

            if self.app.active_entry:
                self.elapsed_seconds = self.app.active_entry.calculate_current_elapsed()
                elapsed_label.update(format_elapsed_time(self.elapsed_seconds))

            button.label = "Stop"
            button.variant = "error"
        else:
            status_label.update("Status: [dim]IDLE[/dim]")
            project_label.update("Project: -")
            elapsed_label.update("00:00:00")
            button.label = "Start"
            button.variant = "success"

    def action_show_reports(self) -> None:
        """Show the reports screen."""
        from .summary_screen import SummaryScreen
        self.app.push_screen(SummaryScreen())
