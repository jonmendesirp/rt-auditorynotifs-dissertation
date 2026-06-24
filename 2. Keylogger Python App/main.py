import os
import keyboard # being used by on_key_press
from datetime import datetime
import keylogger_gui
from hotkey import hot

app = None  # Global reference to the app instance

def create_log_file():
    """Creates a log file with a timestamped name."""  
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/keylog_{timestamp}.txt"
    
    os.makedirs("logs", exist_ok=True)  # create folder if it doesn't exist
    open(filename, "w").close()         # actually create the file

    print(f"Log file created: {filename}")
    return filename

def on_key_press(event):
    """Callback function to handle key press events."""  
    global app
    if app.enabled:
        ##timestamp = datetime.now().strftime("%H:%M:%S:%f")[:-3]  # HH:MM:SS:MMM
        timestamp = app.get_timer()  # Get the timer value from the app
        this_session_file = app.session_file  # Get the current session file from the app
        if(event.name == hot.current_hotkey):
            open(this_session_file, "a").write(f"Hotkey: {event.name} at {timestamp}\n")
            keylogger_gui.KeyloggerApp.update_flags(app, timestamp)  # Update the flag labels in the GUI
            print(f"Hotkey pressed: {event.name} at {timestamp}. written to {this_session_file}")
        else:
            print(f"Key pressed: {event.name} at {timestamp}")
        

if __name__ == "__main__":
    app = keylogger_gui.KeyloggerApp(on_key_press)
    app.run()
