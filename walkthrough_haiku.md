# TimeTracker4 Application Flow Walkthrough
## A Guide for Junior Programmers

Welcome! This document walks through how the entire TimeTracker4 application works, from when you start it to when you're tracking time and viewing reports.

---

## What Does This Application Do?

TimeTracker4 is a **terminal-based time tracking tool**. Think of it like a digital stopwatch for your projects. You can:
- Start/stop tracking time on different projects
- Keep tracking even if you close the app (it remembers!)
- View reports showing how much time you spent on each project
- See detailed history of all your time sessions

---

## The Big Picture: How Everything Connects

```
┌─────────────────────────────────────┐
│   USER (Your Terminal)              │
│   Presses keys, sees output         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   UI LAYER (What you see)           │
│   - Main screen (start/stop)        │
│   - Summary report screen           │
│   - Detail report screen            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   SERVICE LAYER (Business Logic)    │
│   - Tracking service (logic)        │
│   - Project service (load projects) │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   DATABASE LAYER (Saving data)      │
│   - SQLite database                 │
│   - Repositories (read/write)       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   SQLITE DATABASE (The file)        │
│   - Stores tracking sessions        │
│   - Stores start/stop events        │
└─────────────────────────────────────┘
```

**Key Idea**: Information flows DOWN through the layers. The UI never talks directly to the database. Everything goes through the services.

---

## Step-by-Step: When You Start the App

### 1. **You run: `python -m src.main`**

This tells Python to:
- Find the `src` package
- Run the `main.py` file

### 2. **main.py creates the app**

```python
def main():
    app = TimeTrackerApp()  # Create the app
    app.run()              # Start it
```

Think of `TimeTrackerApp` as the "brain" of the entire application. It's a special class from a library called Textual that handles terminal UIs.

### 3. **The app initializes itself (on_mount)**

When the app starts, it automatically runs a special function called `on_mount()`. This is where setup happens:

```
on_mount() runs:
  ├─ Initialize the database
  │  └─ SQLite file is created if it doesn't exist
  │
  ├─ Load projects from file
  │  └─ Read data/projects.txt
  │
  ├─ Check for active tracking
  │  └─ Look in database for ongoing sessions
  │
  └─ Show the Main Screen
     └─ User sees the UI
```

### 4. **Main Screen appears**

You see:
- A dropdown menu to pick your project
- A big button that says "Start" (green)
- Options to view reports

---

## Workflow 1: Starting to Track Time

Let's say you want to track time on your "Website Project":

```
Step 1: SELECT PROJECT
  └─ You click/type to choose "Website Project"

Step 2: PRESS 's' or CLICK START
  └─ This triggers: action_toggle_tracking()

Step 3: SERVICE LOGIC RUNS
  ├─ Check: Is something else already being tracked?
  │  └─ If yes, stop that first
  │
  ├─ Create a TRANSACTION record
  │  └─ Says: "At 3:45 PM, Website Project STARTED"
  │
  └─ Create a TRACKING ENTRY
     └─ Says: "Website Project started at 3:45 PM, not yet stopped"

Step 4: SAVE TO DATABASE
  └─ Both records are saved to SQLite

Step 5: UI UPDATES
  ├─ Button changes to red and says "Stop"
  ├─ A timer appears showing: 0:00, 0:01, 0:02...
  └─ Every second the timer ticks up
```

**Behind the scenes**: A "reactive" timer is running. This means the UI automatically updates every second without you doing anything.

---

## Workflow 2: Stopping Time Tracking

You've been working for 30 minutes. Now you want to stop:

```
Step 1: PRESS 's' or CLICK STOP
  └─ This triggers: action_toggle_tracking() again

Step 2: SERVICE LOGIC RUNS
  ├─ Find the active session
  │  └─ Query database: "Show me tracking entries with NO stop time"
  │
  ├─ Calculate elapsed time
  │  └─ 30 minutes = 1800 seconds
  │
  ├─ Create a TRANSACTION record
  │  └─ Says: "At 4:15 PM, Website Project STOPPED"
  │
  └─ UPDATE the TRACKING ENTRY
     ├─ Add the stop time (4:15 PM)
     └─ Add the duration (1800 seconds)

Step 3: SAVE TO DATABASE
  └─ Both records are updated in SQLite

Step 4: UI UPDATES
  ├─ Button changes back to green and says "Start"
  ├─ Timer stops
  └─ Your session is now saved and complete
```

**Key insight**: A completed session has:
- Start time ✓
- Stop time ✓
- Duration ✓

An active session has:
- Start time ✓
- Stop time ✗ (NULL)
- Duration ✗ (NULL)

---

## Workflow 3: The Magic - Persistent Tracking

This is the cool part. Let's say you're tracking time and you close the app:

```
BEFORE CLOSING:
  ├─ You're tracking "Website Project"
  ├─ It's been 10 minutes
  └─ The tracking entry in the database has:
     ├─ startTime: 3:45 PM
     ├─ stopTime: NULL (not stopped yet)
     └─ timeElapsed: NULL (still going)

YOU CLOSE THE APP
  └─ The data stays in the database!

YOU REOPEN THE APP
  └─ on_mount() runs again

CHECK FOR ACTIVE SESSIONS:
  ├─ Query database: "Show sessions with stopTime = NULL"
  ├─ Found one! "Website Project started at 3:45 PM"
  └─ Still going? Check: current_time - start_time = elapsed

DISPLAY ON MAIN SCREEN:
  ├─ "Tracking: Website Project"
  ├─ Timer shows: 10:05, 10:06... (counting from when it started)
  └─ Red "Stop" button ready to click
```

**Why this is useful**: If your app crashes or you accidentally close it, your work session isn't lost. The timer keeps going from where it left off!

---

## Workflow 4: View Summary Report

You want to see total time tracked per project:

```
Step 1: PRESS 'r' on Main Screen
  └─ This shows the Summary Screen

Step 2: SERVICE LOGIC RUNS
  ├─ Look at ALL completed tracking entries
  ├─ Group them by project
  ├─ Add up the durations for each project
  └─ If a project is actively being tracked, add its current elapsed time

Step 3: FORMAT THE DATA
  └─ Convert seconds to readable format (like "2h 30m")

Step 4: DISPLAY TABLE
  ├─ Website Project:     2h 30m
  ├─ Admin Dashboard:     1h 15m
  ├─ Bug Fixes:           45m
  └─ TOTAL:               4h 30m (all projects combined)
```

The report is sorted by time (most time first) so you see your biggest projects at the top.

---

## Workflow 5: View Detailed History

You want to see every individual session:

```
Step 1: FROM SUMMARY SCREEN, PRESS 'd'
  └─ This shows the Detail Screen

Step 2: SERVICE LOGIC RUNS
  ├─ Retrieve ALL tracking entries
  ├─ Sort by start time (newest first)
  └─ If you filter by project, show only that project

Step 3: DISPLAY TABLE
  ├─ Start Time  │ Stop Time  │ Duration │ Project
  ├─ 4:15 PM    │ 4:45 PM   │ 30m      │ Website
  ├─ 3:00 PM    │ 3:45 PM   │ 45m      │ Admin
  ├─ [Active]   │ ---       │ 2m       │ Website
  └─ 2:00 PM    │ 2:30 PM   │ 30m      │ Bugs
```

Notice:
- Completed sessions show start time, stop time, and duration
- Active sessions show "[Active]" instead of a stop time
- The duration for active sessions is "live" - it updates every second

---

## The Database: Where Data Lives

TimeTracker4 uses SQLite to save everything. Think of it as an Excel spreadsheet, but more powerful.

### Table 1: `transactions` (Audit Log)

This table records every "event" that happens:

```
transactionId │ action │ timeStamp        │ projectName
──────────────┼────────┼──────────────────┼─────────────
1             │ Start  │ 1733289900 (3PM) │ Website
2             │ Stop   │ 1733290700 (3:15)│ Website
3             │ Start  │ 1733290800       │ Admin
4             │ Stop   │ 1733291400       │ Admin
```

**Why track events?** It's like a history book. If something goes wrong, you can look back and see exactly what happened and when.

### Table 2: `timeTracking` (Session Records)

This table stores complete sessions:

```
entryId │ projectName │ startTime │ stopTime │ timeElapsed
────────┼─────────────┼───────────┼──────────┼────────────
1       │ Website     │ 1733289900│ 1733290700│ 800 (seconds)
2       │ Admin       │ 1733290800│ 1733291400│ 600
3       │ Website     │ 1733300000│ NULL     │ NULL
```

Notice entry 3:
- `startTime`: Has a value (session started)
- `stopTime`: NULL (session hasn't ended)
- `timeElapsed`: NULL (not calculated yet)

This NULL pattern is how the app detects "is something currently being tracked?"

---

## Key Concepts Explained Simply

### 1. **Reactive Properties**

```python
is_tracking = reactive(False)  # Starts as False
elapsed_seconds = reactive(0)   # Starts as 0
```

"Reactive" means: "When this value changes, automatically update the UI"

So when you start tracking:
```
is_tracking changes: False → True
├─ The button automatically changes color to red
└─ A timer automatically starts counting up
```

You don't have to write code to update the UI. It happens automatically!

### 2. **The Service Layer**

Services are like "logic helpers". They take requests from the UI and handle the complicated business rules:

```
UI says: "User clicked start"
  ↓
Service checks:
  ├─ Is something already being tracked? If yes, stop it first
  ├─ Is the project valid?
  └─ Can we write to the database?
  ↓
If everything is OK:
  ├─ Create database records
  ├─ Return success
  └─ UI updates itself (because reactive)

If something is wrong:
  └─ Return error message
```

This separation is important. The UI doesn't know HOW to track time. It just asks the service.

### 3. **Repositories**

Repositories are "database helpers". They know how to:
- Save data to SQLite
- Retrieve data from SQLite
- Query data with specific conditions

The service doesn't talk directly to the database. It asks the repository:
```
Service: "Give me all tracking entries for Website project"
  ↓
Repository: "Let me query the database..."
  ↓
Repository: "Here's what I found: [list of entries]"
```

---

## The Flow Chart: Complete Journey

Here's the complete journey from start to finish:

```
USER STARTS APP
└─ Runs: python -m src.main

MAIN.PY
└─ Creates TimeTrackerApp instance

APP INITIALIZATION (on_mount)
├─ Initialize database (SQLite file created)
├─ Load projects from data/projects.txt
├─ Check for active sessions in database
└─ Show Main Screen

MAIN SCREEN DISPLAYED
├─ Dropdown to select project
├─ Green "Start" button
├─ Keyboard shortcuts displayed
└─ User ready to act

USER SELECTS PROJECT AND PRESSES 's'
│
├─ UI LAYER: action_toggle_tracking() called
│   └─ Check: is_tracking status
│
└─ SERVICE LAYER: tracking_service.start_tracking()
    ├─ Check for other active sessions
    ├─ Create transaction record (Start event)
    ├─ Create tracking entry (NULL stop time)
    └─ Return success
        │
        └─ DATABASE LAYER
            ├─ transaction_repo.add() saves event
            ├─ tracking_repo.add() saves session
            └─ SQLite file updated

UI AUTOMATICALLY UPDATES (Reactive)
├─ is_tracking changes to True
├─ Button turns red, says "Stop"
├─ Timer starts: 0:00, 0:01, 0:02...
└─ elapsed_seconds updates every second

USER WORKS FOR 30 MINUTES
└─ Timer shows: 30:00

USER PRESSES 's' TO STOP
│
├─ UI LAYER: action_toggle_tracking() called
│   └─ Check: is_tracking status (True)
│
└─ SERVICE LAYER: tracking_service.stop_tracking()
    ├─ Find active session
    ├─ Calculate: stopTime - startTime
    ├─ Create transaction record (Stop event)
    ├─ Update tracking entry (add stop time & duration)
    └─ Return updated entry
        │
        └─ DATABASE LAYER
            ├─ transaction_repo.add() saves event
            ├─ tracking_repo.update() saves stop time
            └─ SQLite file updated

UI AUTOMATICALLY UPDATES
├─ is_tracking changes to False
├─ Button turns green, says "Start"
├─ Timer stops
└─ Session is complete and saved

USER PRESSES 'r' FOR REPORTS
│
└─ SERVICE LAYER: tracking_service.get_summary_report()
    ├─ Query all completed sessions
    ├─ Group by project name
    ├─ Sum durations for each project
    ├─ Include current elapsed time from active sessions
    └─ Return report data
        │
        └─ DATABASE LAYER
            └─ tracking_repo.query() retrieves data

SUMMARY SCREEN SHOWS TABLE
├─ Website Project: 2h 30m
├─ Admin: 1h 15m
└─ TOTAL: 3h 45m

USER CAN NAVIGATE
├─ Press 'd' to see detail view
├─ Press 'm' to go back to main
└─ Press 'q' to quit
```

---

## File Organization

```
timetracker4/
│
├─ src/
│  ├─ main.py                    ← Entry point (starts here)
│  ├─ app.py                     ← Main app class (the brain)
│  │
│  ├─ ui/
│  │  └─ screens/
│  │     ├─ main_screen.py       ← Start/stop tracking UI
│  │     ├─ summary_screen.py    ← Reports UI
│  │     └─ detail_screen.py     ← History UI
│  │
│  ├─ services/
│  │  ├─ tracking_service.py     ← Tracking logic
│  │  └─ project_service.py      ← Project management
│  │
│  ├─ database/
│  │  ├─ db_manager.py           ← Database connection
│  │  ├─ tracking_repo.py        ← Tracking data access
│  │  ├─ transaction_repo.py     ← Event data access
│  │  └─ schema.py               ← Database structure
│  │
│  ├─ models/
│  │  ├─ tracking_entry.py       ← Time session object
│  │  └─ transaction.py          ← Event object
│  │
│  └─ utils/
│     ├─ constants.py            ← App constants
│     └─ time_utils.py           ← Time formatting
│
└─ data/
   └─ projects.txt               ← List of projects

timetracker.db                   ← SQLite database file (created)
```

---

## Common Questions Junior Programmers Ask

### Q: Why separate the service layer?
**A**: So the UI doesn't need to know how to track time. The service handles all the business logic. If you wanted to add a web UI later, you could reuse the same services!

### Q: Why use repositories?
**A**: If you ever wanted to switch databases (SQLite to PostgreSQL), you'd only need to change the repository code. The service layer wouldn't change.

### Q: How does the timer update?
**A**: Textual (the terminal UI library) has a built-in timer that ticks every second. When `elapsed_seconds` is reactive, the UI automatically re-renders.

### Q: What happens if the app crashes?
**A**: The database already has all the data saved. When you restart:
1. `on_mount()` looks for active sessions (stopTime = NULL)
2. It finds your session and continues from where it left off
3. The timer uses the original start time, so it shows the correct elapsed duration

### Q: Can multiple projects be tracked at once?
**A**: No, the design allows only one active session. If you start tracking a new project while one is active, the old one is automatically stopped first.

---

## Summary

TimeTracker4 is built with **layers** that each have one job:

1. **UI Layer**: Shows information and gets user input
2. **Service Layer**: Contains all the business logic
3. **Database Layer**: Saves and retrieves data
4. **Database**: Actually stores everything

Each layer talks to the layer below it, which makes the code organized and maintainable.

The key workflows are:
- **Start**: Press 's' → service creates records → database saves → UI updates
- **Stop**: Press 's' → service updates records → database saves → UI updates
- **Reports**: Press 'r' → service queries data → database returns data → UI displays
- **Persistence**: Active sessions stay in database even if app closes

This design means the app can reliably track time and survive crashes!
