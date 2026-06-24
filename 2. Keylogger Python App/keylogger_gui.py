import keyboard
import tkinter as tk
import time
import os
from datetime import datetime
from hotkey import HotkeyManager, hot
import main as m 

class KeyloggerApp:
    """A simple GUI application to toggle keylogging on and off."""

    def __init__(self, callback):
        self.callback = callback
        self.enabled = False
        self.hotkey_manager = hot
        hot.set_callback(self.toggle)
        self.root = tk.Tk()
        self.root.title("Keylogger Toggle")
        self.root.geometry("250x300")

        self.keybind_label = tk.Label(self.root, text="Hotkey (press to record):")
        self.keybind_label.pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        self.record_hotkey_button = tk.Button(button_frame, text="Record Hotkey", command=self.record_hotkey)
        self.record_hotkey_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reset Hotkey", command=self.reset_hotkey, state='disabled')
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.toggle_button = tk.Button(self.root, text="Start Keylogger", command=self.toggle)
        self.toggle_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Disabled")
        self.status_label.pack()

        self.timer_label = tk.Label(self.root, text="00:00:00:000", font=("Arial", 24))
        self.timer_label.pack(pady=10)

        self.flag_label_youngest = tk.Label(self.root, text="--", fg="gray")
        self.flag_label_youngest.pack(pady=0)

        self.flag_label_middle = tk.Label(self.root, text="--", fg="gray")
        self.flag_label_middle.pack(pady=0)

        self.flag_label_oldest = tk.Label(self.root, text="--", fg="gray")
        self.flag_label_oldest.pack(pady=2)

        self.flag_labels = [self.flag_label_youngest, self.flag_label_middle, self.flag_label_oldest]

        self.start_time = None
        self.current_flag = 0

        self.update_timer()  # Start the clock

    def record_hotkey(self):
        """Start recording a hotkey combination."""
        self.hotkey_manager.record_hotkey(self.keybind_label, self.record_hotkey_button, self.reset_button)

    def reset_hotkey(self):
        """Reset the current hotkey."""
        self.hotkey_manager.reset_hotkey()

    def toggle(self):
        """Toggle the keylogger on or off."""
        self.enabled = not self.enabled
        if self.enabled:
            self.start_time = datetime.now()
            self.session_file = m.create_log_file()
            keyboard.on_press(self.callback)
            self.status_label.config(text="Enabled", fg="green")
            self.timer_label.config(fg="green")
            self.toggle_button.config(text="Stop Keylogger")
        else:
            self.start_time = None
            keyboard.unhook_all()
            self.status_label.config(text="Disabled", fg="black")
            self.timer_label.config(text="00:00:00:000", fg="black")
            self.toggle_button.config(text="Start Keylogger")
            self.current_flag = 0

    def update_timer(self):
        """Update the count-up timer display."""
        if self.enabled and self.start_time is not None:
            time_str = self.get_timer()
            self.timer_label.config(text=time_str)
        self.root.after(10, self.update_timer)

    def get_timer(self):
        """Get the current timer value as a string."""
        if self.start_time is None:
            return "00:00:00:000"
        elapsed = datetime.now() - self.start_time
        total_seconds = int(elapsed.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        milliseconds = elapsed.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    
    def write_time(self, index, timestamp):
        self.flag_labels[index].config(text=f"Flag {self.current_flag + 1}: Pressed at: {timestamp}")
    
    def update_flags(self, timestamp):
        """Update the flag labels with the most recent key presses."""

        if self.current_flag > 2:
            self.flag_index = 2

            for i in range(len(self.flag_labels) - 1):
                next_flag_text = self.flag_labels[i+1].cget("text")
                self.flag_labels[i].config(text=next_flag_text) 

        else:
            self.flag_index = self.current_flag
            

        self.write_time(self.flag_index, timestamp)
        self.current_flag += 1

    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()

    def set_callback(self, callback):
        self.toggle_callback = callback

