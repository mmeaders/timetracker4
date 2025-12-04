# Time Tracker TUI

A compact, terminal-based time tracking application built with Python and Textual.

## Features

- Track time spent on projects with start/stop functionality
- Persistent tracking - time continues running even when app is closed
- SQLite database storage for all tracking data
- Summary reports showing total time per project
- Detailed session history with filtering
- Compact, calculator-sized interface
- Keyboard shortcuts for quick navigation

## Requirements

- Python 3.8+
- Textual >= 0.47.0

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python -m src.main
```

### Managing Projects

Projects are managed by editing the `data/projects.txt` file. Add one project name per line:

```
Client Website
Internal Tools
Research
Documentation
Testing
```

The file is created automatically with sample projects on first run if it doesn't exist.

### Tracking Time

1. **Start Tracking:**
   - Select a project from the dropdown
   - Click "Start" button or press `s`
   - Time begins tracking immediately

2. **Stop Tracking:**
   - Click "Stop" button or press `s`
   - Session is saved to database

3. **Persistent Tracking:**
   - If you close the app while tracking, time continues running
   - When you reopen the app, it resumes from where you left off
   - Only one project can be tracked at a time

### Viewing Reports

1. **Summary Report:**
   - Shows total time spent on each project
   - Press `r` from main screen or click "Reports"
   - Sorted by total time (highest first)

2. **Detail Report:**
   - Shows individual tracking sessions
   - Filter by specific project or view all
   - Displays start/stop times and duration
   - Active sessions shown with "Active" status

### Keyboard Shortcuts

**Main Screen:**
- `s` - Start/Stop tracking
- `r` - Show reports
- `q` - Quit application

**Summary Screen:**
- `m` - Return to main screen
- `d` - Show detail screen
- `escape` - Go back

**Detail Screen:**
- `m` - Return to main screen
- `s` - Show summary screen
- `escape` - Go back

## Database Schema

The application uses SQLite with two tables:

### transactions
Records each start/stop event:
- `transactionId` - Sequential ID
- `action` - 'Start' or 'Stop'
- `timeStamp` - Unix timestamp
- `projectName` - Name of project

### timeTracking
Records completed and active tracking sessions:
- `entryId` - Sequential ID
- `projectName` - Name of project
- `startTime` - Unix timestamp when started
- `stopTime` - Unix timestamp when stopped (NULL if active)
- `timeElapsed` - Total seconds (NULL if active)

## File Structure

```
timetracker4/
├── src/
│   ├── database/       # Database layer
│   ├── models/         # Data models
│   ├── services/       # Business logic
│   ├── ui/             # User interface
│   │   └── screens/    # Screen components
│   ├── utils/          # Utilities
│   ├── app.py          # Main app class
│   ├── main.py         # Entry point
│   └── styles.css      # TUI styling
├── data/
│   ├── projects.txt    # Project list
│   └── timetracker.db  # SQLite database
└── requirements.txt
```

## Data Location

- Projects file: `data/projects.txt`
- Database: `data/timetracker.db`

Both files are created automatically in the `data/` directory on first run.

## Troubleshooting

**"Already tracking" warning:**
- You can only track one project at a time
- Stop the current project before starting another

**Projects not showing:**
- Check that `data/projects.txt` exists and has project names (one per line)
- Restart the application after editing the file

**Database errors:**
- Ensure the `data/` directory is writable
- Check that `data/timetracker.db` is not locked by another process

## License

This project is open source and available for personal and commercial use.
