# Climbing Progression Tracker

A desktop application built with Python and Tkinter that allows climbers to record their climbing sessions, review previous sessions, and track their climbing history.

## Features

- Add climbing sessions with dates, locations, climbing types, grades, attempts, and notes.
- View previously recorded climbing sessions.
- Filter sessions by climbing type and sort by date.
- View and edit existing session details.
- Validate user input to prevent invalid information from being saved.
- Confirm before discarding unsaved changes.
- Save session information locally using JSON.

## Requirements

- Python 3
- Tkinter (included with many Python installations)

## How to Run

1. Download or clone the repository.
2. Open the project folder.
3. Run the following command:

```bash
python3 main.py
```

## Data Storage

Climbing sessions are stored locally in `sessions.json`. Data does not automatically synchronize between devices. Back up this file to preserve your climbing history.

## Project Information

Developed as an individual project for CS361: Software Engineering I at Oregon State University.