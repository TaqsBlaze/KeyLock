import ctypes
import pythoncom
import pyWinhook

# This function will be called on each key press
class KeyboardBlocker:
    def __init__(self):
        self.hm = pyWinhook.HookManager()
        self.hm.KeyDown = self.on_keyboard_event
        self.hm.HookKeyboard()
        self.is_blocking = True  # Flag to indicate if blocking is active
    
    def on_keyboard_event(self, event):
        if event.Key == 'Escape':
            return True  # Allow Escape key
        else:
            print(f"Blocked key: {event.Key}")  # Log blocked keys
            return False  # Block all other keys

    def start(self):
        pythoncom.PumpMessages()

    def unhook(self):
        if self.is_blocking:
            self.hm.UnhookKeyboard()
            self.is_blocking = False
            print("Keyboard unhooked.")