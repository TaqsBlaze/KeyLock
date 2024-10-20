from PyQt5.QtWidgets import QMainWindow, QApplication, QCheckBox, QPushButton
from PyQt5 import uic, QtWidgets, QtCore
from pynput import keyboard
from resources import resources
import sys
import threading


class KeyLockerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file
        uic.loadUi('resources/ui/main.ui', self)
        self.toggle = self.findChild(QCheckBox, "toggle")
        self.closebtn = self.findChild(QPushButton, "closeButton")
        self.toggle.stateChanged.connect(self.toggle_keyboard_lock)
        self.closebtn.clicked.connect(self.close_application)
        # Transparent and frameless window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.listener = None
        self.blocking = False  # Flag to indicate if blocking is active

    def close_application(self):
        if self.listener is not None and self.listener.is_alive():
            self.listener.stop()
        QtWidgets.QApplication.quit()

    def toggle_keyboard_lock(self, state):
        if state == QtCore.Qt.Checked:
            self.start_listener()
            self.blocking = True
        else:
            if self.listener is not None and self.listener.is_alive():
                self.listener.stop()
                self.listener = None
            self.blocking = False

    def start_listener(self):
        def on_press(key):
            if self.blocking and key != keyboard.Key.esc:
                return False  # Block all keys except ESC
            return True  # Allow ESC to exit the listener

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()  # Start the listener in a non-blocking way

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KeyLockerApp()
    window.show()
    sys.exit(app.exec_())
