# Name: Michael Breaux
# Course: CS361 - Software Engineering I
# Assignment: 5 - Main Program Implementation
# Description: Climbing Progression Tracker application.
# Allows users to log, view, and edit climbing sessions.

import tkinter as tk
import json
from pathlib import Path
from datetime import datetime
from tkinter import messagebox


# File used to store climbing sessions
DATA_FILE = Path(__file__).with_name("sessions.json")


def save_session(session):
    """Save a new climbing session to the JSON file."""

    # Load previously saved sessions
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            sessions = json.load(file)
    else:
        sessions = []

    # Add the new session
    sessions.append(session)

    # Save the updated list
    with open(DATA_FILE, "w") as file:
        json.dump(sessions, file, indent=4)



def load_sessions():
    """Load previously saved climbing sessions."""

    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    return []


def validate_session(date, location, grade, attempts, window):
    """Check required values and return the attempts as an integer."""
    if not date or not location or not grade or not attempts:
        messagebox.showerror("Missing Information",
                             "Please enter a date, location, grade, and number of attempts.",
                             parent=window)
        return None
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        if parsed_date.strftime("%Y-%m-%d") != date:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Date", "Enter a real date in YYYY-MM-DD format.",
                             parent=window)
        return None
    if not attempts.isdecimal() or int(attempts) < 1:
        messagebox.showerror("Invalid Attempts",
                             "Number of attempts must be a positive whole number (1 or more).",
                             parent=window)
        return None
    return int(attempts)


def confirm_discard(window, changed):
    """Show clearly named choices before discarding unsaved work."""
    if not changed():
        window.destroy()
        return

    dialog = tk.Toplevel(window)
    dialog.title("Unsaved Changes")
    dialog.resizable(False, False)
    dialog.transient(window)
    dialog.grab_set()
    tk.Label(dialog, text="You have unsaved changes.",
             font=("Arial", 14, "bold")).pack(padx=30, pady=(25, 8))
    tk.Label(dialog, text="Would you like to keep editing or discard your changes?",
             font=("Arial", 11), wraplength=350).pack(padx=25, pady=(0, 20))

    def keep_editing():
        dialog.destroy()
        window.focus_set()

    def discard_changes():
        dialog.destroy()
        window.destroy()

    tk.Button(dialog, text="Keep Editing", font=("Arial", 12),
              width=22, command=keep_editing).pack(pady=5)
    tk.Button(dialog, text="Discard Changes", font=("Arial", 12),
              width=22, command=discard_changes).pack(pady=(5, 22))
    dialog.protocol("WM_DELETE_WINDOW", keep_editing)
    dialog.bind("<Escape>", lambda event: keep_editing())
    dialog.update_idletasks()
    dialog.geometry(f"+{window.winfo_rootx() + 70}+{window.winfo_rooty() + 100}")
    dialog.focus_set()


def open_add_session():
    """Open the form for recording a new climbing session."""

    add_window = tk.Toplevel()
    add_window.title("Add Climbing Session")
    add_window.geometry("550x750")

    # Form heading
    tk.Label(
        add_window,
        text="Add New Climbing Session",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    # Date
    tk.Label(
        add_window,
        text="Date (YYYY-MM-DD):",
        font=("Arial", 12)
    ).pack(pady=5)

    date_entry = tk.Entry(add_window, font=("Arial", 12), width=30)
    date_entry.pack(pady=5)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    # Location
    tk.Label(
        add_window,
        text="Climbing Location:",
        font=("Arial", 12)
    ).pack(pady=5)

    location_entry = tk.Entry(add_window, font=("Arial", 12), width=30)
    location_entry.pack(pady=5)

    # Climbing type
    tk.Label(
        add_window,
        text="Climbing Type:",
        font=("Arial", 12)
    ).pack(pady=5)

    climbing_type = tk.StringVar(value="Bouldering")

    type_menu = tk.OptionMenu(
        add_window, climbing_type, "Bouldering", "Rope"
    )
    type_menu.config(font=("Arial", 12), width=25)
    type_menu.pack(pady=5)

    # Grade
    tk.Label(
        add_window,
        text="Climbing Grade:",
        font=("Arial", 12)
    ).pack(pady=5)

    grade_entry = tk.Entry(add_window, font=("Arial", 12), width=30)
    grade_entry.pack(pady=5)

    # Attempts
    tk.Label(
        add_window,
        text="Number of Attempts:",
        font=("Arial", 12)
    ).pack(pady=5)

    attempts_entry = tk.Entry(add_window, font=("Arial", 12), width=30)
    attempts_entry.pack(pady=5)

    # Notes
    tk.Label(
        add_window,
        text="Session Notes (Optional):",
        font=("Arial", 12)
    ).pack(pady=5)

    notes_entry = tk.Text(
        add_window,
        font=("Arial", 12),
        width=30,
        height=4
    )
    notes_entry.pack(pady=5)

    def handle_save():
        """Check the form and save the session."""

        date = date_entry.get().strip()
        location = location_entry.get().strip()
        grade = grade_entry.get().strip()
        attempts = attempts_entry.get().strip()
        notes = notes_entry.get("1.0", tk.END).strip()

        attempts_number = validate_session(date, location, grade, attempts, add_window)
        if attempts_number is None:
            return

        # Create the session record
        session = {
            "date": date,
            "location": location,
            "type": climbing_type.get(),
            "grade": grade,
            "attempts": attempts_number,
            "notes": notes
        }

        # Save the session
        try:
            save_session(session)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            messagebox.showerror(
                "Save Failed",
                f"Could not save the session: {error}",
                parent=add_window
            )
            return

        messagebox.showinfo(
            "Session Saved",
            "Your climbing session was saved successfully!",
            parent=add_window
        )
        add_window.destroy()

    def current_form():
        return (date_entry.get(), location_entry.get(), climbing_type.get(),
                grade_entry.get(), attempts_entry.get(),
                notes_entry.get("1.0", "end-1c"))

    original_form = current_form()

    def cancel_add():
        confirm_discard(add_window, lambda: current_form() != original_form)

    add_window.protocol("WM_DELETE_WINDOW", cancel_add)
    add_window.bind("<Escape>", lambda event: cancel_add())
    add_window.bind("<Control-Return>", lambda event: handle_save())
    add_window.bind("<Command-Return>", lambda event: handle_save())
    location_entry.focus_set()

    # Save button
    tk.Button(
        add_window,
        text="Save Session",
        font=("Arial", 12),
        width=20,
        command=handle_save
    ).pack(pady=(20, 5))

    # Cancel button
    tk.Button(
        add_window,
        text="Cancel",
        font=("Arial", 12),
        width=20,
        command=cancel_add
    ).pack(pady=5)


def view_sessions():
    """Browse saved sessions with type filtering and date sorting."""
    try:
        sessions = load_sessions()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        messagebox.showerror("Unable to Load Sessions", str(error))
        return

    view_window = tk.Toplevel()
    view_window.title("Previous Climbing Sessions")
    view_window.geometry("850x650")
    tk.Label(view_window, text="Previous Climbing Sessions",
             font=("Arial", 18, "bold")).pack(pady=(22, 12))

    controls = tk.Frame(view_window)
    controls.pack(pady=8)
    tk.Label(controls, text="Climbing type:", font=("Arial", 12)).grid(
        row=0, column=0, padx=(0, 8))
    filter_type = tk.StringVar(value="All Sessions")
    tk.OptionMenu(controls, filter_type, "All Sessions", "Bouldering", "Rope").grid(
        row=0, column=1, padx=(0, 24))
    tk.Label(controls, text="Sort by date:", font=("Arial", 12)).grid(
        row=0, column=2, padx=(0, 8))
    sort_order = tk.StringVar(value="Newest First")
    tk.OptionMenu(controls, sort_order, "Newest First", "Oldest First").grid(
        row=0, column=3)

    tk.Label(view_window, text="Select a session to view its details (or double-click).",
             font=("Arial", 11)).pack(pady=(4, 6))
    list_frame = tk.Frame(view_window)
    list_frame.pack(fill="both", expand=True, padx=35, pady=(0, 8))
    session_list = tk.Listbox(list_frame, font=("Arial", 12),
                              selectmode=tk.SINGLE, exportselection=False)
    scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=session_list.yview)
    session_list.configure(yscrollcommand=scrollbar.set)
    session_list.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    count_label = tk.Label(view_window, font=("Arial", 11))
    count_label.pack(pady=4)
    visible_indexes = []

    def refresh_list(*args):
        """Rebuild the list while keeping original JSON indexes intact."""
        selected_index = None
        if session_list.curselection():
            position = session_list.curselection()[0]
            if position < len(visible_indexes):
                selected_index = visible_indexes[position]
        session_list.delete(0, tk.END)
        visible_indexes.clear()
        matching = [(i, item) for i, item in enumerate(sessions)
                    if filter_type.get() == "All Sessions"
                    or item.get("type") == filter_type.get()]
        matching.sort(key=lambda pair: (str(pair[1].get("date", "")), pair[0]),
                      reverse=sort_order.get() == "Newest First")
        for index, item in matching:
            visible_indexes.append(index)
            session_list.insert(tk.END,
                f"{item.get('date', '')}  |  {item.get('location', '')}  |  "
                f"{item.get('type', '')}  |  {item.get('grade', '')}")
        count_label.config(text=f"Showing {len(matching)} of {len(sessions)} sessions")
        if selected_index in visible_indexes:
            position = visible_indexes.index(selected_index)
            session_list.selection_set(position)
            session_list.see(position)

    filter_type.trace_add("write", refresh_list)
    sort_order.trace_add("write", refresh_list)
    refresh_list()

    def show_details():
        selection = session_list.curselection()
        if not selection:
            messagebox.showwarning("No Session Selected",
                                   "Please select a session first.", parent=view_window)
            return
        index = visible_indexes[selection[0]]
        session = sessions[index]
        details_window = tk.Toplevel(view_window)
        details_window.title("Session Details")
        details_window.geometry("550x510")
        tk.Label(details_window, text="Session Details",
                 font=("Arial", 18, "bold")).pack(pady=(20, 15))
        details = (f"Date: {session.get('date', '')}\n\n"
                   f"Location: {session.get('location', '')}\n\n"
                   f"Type: {session.get('type', '')}\n\n"
                   f"Grade: {session.get('grade', '')}\n\n"
                   f"Attempts: {session.get('attempts', '')}\n\n"
                   f"Notes: {session.get('notes', '')}")
        tk.Label(details_window, text=details, font=("Arial", 12),
                 justify="left", wraplength=460).pack(padx=25, pady=10)
        details_window.bind("<Escape>", lambda event: details_window.destroy())
        tk.Button(details_window, text="Edit Session", font=("Arial", 12),
                  width=22, command=lambda: edit_session(
                      index, details_window, view_window)).pack(pady=10)
        tk.Button(details_window, text="Back", font=("Arial", 12),
                  width=22, command=details_window.destroy).pack(pady=5)
        details_window.transient(view_window)
        details_window.focus_set()

    session_list.bind("<Double-Button-1>", lambda event: show_details())
    session_list.bind("<Return>", lambda event: show_details())
    view_window.bind("<Escape>", lambda event: view_window.destroy())
    tk.Button(view_window, text="View Selected Session", font=("Arial", 12),
              width=25, command=show_details).pack(pady=8)
    tk.Button(view_window, text="Close", font=("Arial", 12),
              width=25, command=view_window.destroy).pack(pady=(2, 20))
    session_list.focus_set()


def edit_session(index, details_window, view_window):
    """Allow the user to update an existing session."""

    try:
        sessions = load_sessions()
        session = sessions[index]
    except (OSError, ValueError, IndexError, json.JSONDecodeError) as error:
        messagebox.showerror("Unable to Edit Session", str(error), parent=details_window)
        return

    edit_window = tk.Toplevel()
    edit_window.title("Edit Climbing Session")
    edit_window.geometry("550x700")

    tk.Label(
        edit_window,
        text="Edit Climbing Session",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    # Create fields with existing session information
    entries = {}

    fields = [
        ("date", "Date (YYYY-MM-DD)"),
        ("location", "Climbing Location"),
        ("grade", "Climbing Grade"),
        ("attempts", "Number of Attempts")
    ]

    for key, label in fields:
        tk.Label(
            edit_window,
            text=label,
            font=("Arial", 12)
        ).pack(pady=5)

        entry = tk.Entry(
            edit_window,
            font=("Arial", 12),
            width=30
        )
        entry.insert(0, str(session[key]))
        entry.pack(pady=5)

        entries[key] = entry

    # Climbing type
    tk.Label(
        edit_window,
        text="Climbing Type",
        font=("Arial", 12)
    ).pack(pady=5)

    climbing_type = tk.StringVar(value=session["type"])

    tk.OptionMenu(
        edit_window,
        climbing_type,
        "Bouldering",
        "Rope"
    ).pack(pady=5)

    # Notes
    tk.Label(
        edit_window,
        text="Session Notes",
        font=("Arial", 12)
    ).pack(pady=5)

    notes_entry = tk.Text(
        edit_window,
        font=("Arial", 12),
        width=30,
        height=4
    )
    notes_entry.insert("1.0", session["notes"])
    notes_entry.pack(pady=5)

    def save_changes():
        """Save changes made to the selected session."""

        date = entries["date"].get().strip()
        location = entries["location"].get().strip()
        grade = entries["grade"].get().strip()
        attempts = entries["attempts"].get().strip()

        attempts_number = validate_session(date, location, grade, attempts, edit_window)
        if attempts_number is None:
            return

        sessions[index] = {
            "date": date,
            "location": location,
            "type": climbing_type.get(),
            "grade": grade,
            "attempts": attempts_number,
            "notes": notes_entry.get("1.0", tk.END).strip()
        }

        # Update the JSON file
        try:
            with open(DATA_FILE, "w") as file:
                json.dump(sessions, file, indent=4)
        except OSError as error:
            messagebox.showerror(
                "Save Failed",
                f"Could not save changes: {error}",
                parent=edit_window
            )
            return

        messagebox.showinfo(
            "Changes Saved",
            "Your climbing session has been updated!",
            parent=edit_window
        )

        edit_window.destroy()
        details_window.destroy()
        view_window.destroy()

        view_sessions()

    def current_form():
        return (entries["date"].get(), entries["location"].get(),
                entries["grade"].get(), entries["attempts"].get(),
                climbing_type.get(), notes_entry.get("1.0", "end-1c"))

    original_form = current_form()

    def cancel_edit():
        confirm_discard(edit_window, lambda: current_form() != original_form)

    edit_window.protocol("WM_DELETE_WINDOW", cancel_edit)
    edit_window.bind("<Escape>", lambda event: cancel_edit())
    edit_window.bind("<Control-Return>", lambda event: save_changes())
    edit_window.bind("<Command-Return>", lambda event: save_changes())

    tk.Button(
        edit_window,
        text="Save Changes",
        font=("Arial", 12),
        width=20,
        command=save_changes
    ).pack(pady=15)

    tk.Button(
        edit_window,
        text="Cancel",
        font=("Arial", 12),
        width=20,
        command=cancel_edit
    ).pack(pady=5)


def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Climbing Progression Tracker")
    root.geometry("800x600")

    # Add a title to the window
    title_label = tk.Label(
        root,
        text="Climbing Progression Tracker",
        font=("Arial", 22, "bold")
    )
    title_label.pack(pady=30)

    tk.Label(
        root,
        text="Log your climbs, review past sessions, and track your progress.",
        font=("Arial", 12), wraplength=650
    ).pack(pady=(0, 15))

    # Button to open the Add Session window
    add_button = tk.Button(
        root,
        text="Add Climbing Session",
        font=("Arial", 14),
        width=25,
        command=open_add_session
    )
    add_button.pack(pady=(10, 5))
    tk.Label(root, text="Record a climb's date, location, grade, attempts, and notes.",
             font=("Arial", 11)).pack(pady=(0, 15))


    # Button to view previously saved sessions
    view_button = tk.Button(
        root,
        text="View Previous Sessions",
        font=("Arial", 14),
        width=25,
        command=view_sessions
    )
    view_button.pack(pady=(10, 5))
    tk.Label(root, text="Browse or filter saved sessions, then view or edit details.",
             font=("Arial", 11)).pack(pady=(0, 20))

    tk.Label(root,
             text="Your sessions are stored locally in sessions.json on this computer.",
             font=("Arial", 10), wraplength=650).pack(pady=10)


    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

