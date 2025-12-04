"""Entry point for the time tracker application."""

from .app import TimeTrackerApp


def main():
    """Run the time tracker application."""
    app = TimeTrackerApp()
    app.run()


if __name__ == "__main__":
    main()
