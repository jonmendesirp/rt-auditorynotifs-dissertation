import keyboard

class HotkeyManager:
    """Manages hotkey recording and resetting for the keylogger."""

    MODIFIERS = {'ctrl', 'alt', 'shift', 'windows', 'left ctrl', 'right ctrl',
    'left shift', 'right shift', 'left alt', 'right alt',
    'left windows', 'right windows'}

    def __init__(self, toggle_callback):
        self.toggle_callback = toggle_callback
        self.current_hotkey = None
        self.recording = False
        self.pressed_keys = set()

    def record_hotkey(self, label, record_button, reset_button):
        """Start recording a hotkey combination."""
        self.recording = True
        self.pressed_keys = set()
        keyboard.on_press(self.record_callback)
        keyboard.on_release(self.record_release_callback)
        label.config(text="Press your hotkey combination...")
        record_button.config(state='disabled')
        self.label = label
        self.record_button = record_button
        self.reset_button = reset_button

    def record_callback(self, event):
        """Callback for recording key presses."""
        if self.recording:
            self.pressed_keys.add(event.name)
            if event.name not in self.MODIFIERS:
                # Stop recording and set the hotkey
                hotkey = '+'.join(sorted(self.pressed_keys))
                try:
                    keyboard.add_hotkey(hotkey, self.toggle_callback)
                    keyboard.unhook_all()
                    self.recording = False
                    self.current_hotkey = hotkey
                    self.label.config(text=f"Hotkey set: {hotkey}")
                    self.reset_button.config(state='normal')
                except Exception as e:
                    self.label.config(text=f"Invalid hotkey: {str(e)}")
                    self.recording = False
                    self.record_button.config(state='normal')

    def record_release_callback(self, event):
        """Callback for recording key releases."""
        if self.recording:
            self.pressed_keys.discard(event.name)

    def reset_hotkey(self):
        """Reset the current hotkey."""
        if self.current_hotkey:
            try:
                keyboard.remove_hotkey(self.current_hotkey)
            except:
                pass  # Ignore if not found
            self.current_hotkey = None
            self.label.config(text="Hotkey (press to record):")
            self.record_button.config(state='normal')
            self.reset_button.config(state='disabled')

    def set_callback(self, callback):
        self.toggle_callback = callback


hot = HotkeyManager(lambda: None)

if __name__ == "__main__":
    print(f"Current hotkey: {hot.current_hotkey}")