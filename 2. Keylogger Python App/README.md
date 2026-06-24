# MyKeyLogger

DISCLAIMER: This file was written by Codex

MyKeyLogger is a small Python desktop application for recording timestamped
hotkey events during a timed session. It provides a Tkinter interface for
starting and stopping capture, choosing a hotkey, viewing elapsed time, and
displaying the three most recent markers.

> Use this application only on systems you own or where every affected user
> has explicitly consented. Global keyboard monitoring can expose sensitive
> information and may be restricted by local law or organizational policy.

## Features

- Graphical interface built with Tkinter
- Start and stop controls for recording sessions
- Configurable global hotkey
- Millisecond-resolution session timer
- Timestamped text log for each session
- Display of the three most recent hotkey markers

The application observes all key presses while a session is enabled, but only
the configured hotkey and its timestamp are written to the session log. Other
keys are printed to the terminal for debugging and are not saved to the log.

## Requirements

- Python 3.9 or newer
- Tkinter
- [`keyboard`](https://pypi.org/project/keyboard/) Python package

Tkinter is included with most Windows and macOS Python installations. On some
Linux distributions it must be installed separately.

## Installation

Clone or download the project, open a terminal in its directory, and create an
optional virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate it with:

```powershell
.venv\Scripts\activate
```

Install the external dependency:

```bash
python3 -m pip install keyboard
```

## Running the Application

From the project directory, run:

```bash
python3 main.py
```

Run the command from the project root because session files are written to a
relative `logs/` directory.

### Operating-system permissions

Global keyboard hooks may require additional privileges:

- **macOS:** Grant the terminal or Python process permission under **System
  Settings > Privacy & Security > Accessibility** and, if requested, **Input
  Monitoring**.
- **Linux:** The `keyboard` package may require root access to read input
  devices. Review the package's platform requirements before elevating
  privileges.
- **Windows:** Standard execution usually works, although elevated
  applications may not expose their key events to a non-elevated process.

## Usage

1. Select **Record Hotkey**.
2. Press the desired key or key combination.
3. Select **Start Keylogger** to begin a timed session.
4. Press the configured hotkey to add a timestamped marker.
5. Select **Stop Keylogger** when the session is complete.

The configured hotkey can also toggle the session after it has been registered.
Select **Reset Hotkey** to remove it and record a new one.

Starting a session:

- resets the timer;
- creates a new timestamped file in `logs/`;
- installs a global key-press listener; and
- changes the status indicator to **Enabled**.

Stopping a session removes the keyboard hooks, resets the timer display, and
returns the interface to **Disabled**.

## Log Files

Each session creates a file with this naming pattern:

```text
logs/keylog_YYYY-MM-DD_HH-MM-SS.txt
```

A recorded marker has the following format:

```text
Hotkey: f8 at 00:00:12:347
```

The timestamp represents elapsed session time as:

```text
hours:minutes:seconds:milliseconds
```

Logs are plain text and are not encrypted. Treat them as potentially sensitive
data and do not commit real session logs to source control.

## Project Structure

```text
MyKeyLogger/
├── main.py            # Entry point, session-file creation, and key callback
├── keylogger_gui.py   # Tkinter interface, timer, and marker display
├── hotkey.py          # Hotkey recording, registration, and reset logic
└── logs/              # Generated session logs
```

## How It Works

`main.py` creates a `KeyloggerApp` and supplies the callback invoked for global
key presses. `KeyloggerApp` owns the interface and session state. Its start
control creates a log file and registers the callback through the `keyboard`
package.

`HotkeyManager` records the selected key combination and registers it as a
global hotkey. When the configured marker is detected during an active
session, the callback writes its elapsed timestamp and updates the three marker
labels in the interface.

## Current Limitations

- Hotkeys and preferences are not saved between launches.
- Session logs use a relative path and depend on the launch directory.
- Logging and terminal output use synchronous file and console operations.
- The GUI does not provide a log viewer or export controls.
- Combination hotkeys may not be written as markers reliably because incoming
  key events contain an individual key name while the configured value may be
  a combined string such as `ctrl+f8`.
- Stopping capture calls `keyboard.unhook_all()`, which can also remove the
  registered toggle hotkey.
- Closing the window while capture is active has no dedicated cleanup handler.

## Troubleshooting

### No key events are detected

Confirm that the process has the required accessibility, input-monitoring, or
input-device permissions for the operating system.

### `ModuleNotFoundError: No module named 'keyboard'`

Install the package in the same Python environment used to launch the app:

```bash
python3 -m pip install keyboard
```

### The interface does not open

Verify that Tkinter is available:

```bash
python3 -m tkinter
```

This command should open a small Tkinter test window.

### The log is created in an unexpected location

Launch `main.py` from the project root. The `logs/` path is relative to the
current working directory, not necessarily to the source file.

## Development Notes

There is currently no automated test suite or packaging configuration. A basic
syntax check can be run with:

```bash
python3 -m py_compile main.py keylogger_gui.py hotkey.py
```

