from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFrame,QLabel, QCheckBox, QPushButton
from PyQt5 import uic,QtWidgets, QtCore
from resources import resources
from lock import KeyboardBlocker
import sys
import threading


class KeyLockerApp(QMainWindow):
    
    
    def __init__(self):
        super().__init__()
        # Load the UI file
        uic.loadUi('resources/ui/main.ui', self)
        self.toggle = self.findChild(QCheckBox, "toggle")
        self.closebtn = self.findChild(QPushButton, "closeButton")
        #self.icon = self.findChild(QLabel, "icon")
        self.toggle.stateChanged.connect(self.check_status)
        self.closebtn.clicked.connect(self.close_application)
        self.closebtn.setShortcut("Ctr+X")
        #transparent and frameless window
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.keyboard_blocker = None
        self.blocking_thread = None

        # Variables for dragging
        self.dragging = False
        self.startPos = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.startPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.startPos)
            event.accept()
    def close_application(self):

        QtWidgets.QApplication.quit()


    def check_status(self, state):
 
        if state == 2:
            
            self.keyboard_blocker = KeyboardBlocker()
            self.blocking_thread = threading.Thread(target=self.keyboard_blocker.start)
            self.blocking_thread.daemon = True  # Allows the thread to close when the main program exits
            self.blocking_thread.start()
            QMessageBox.information(self, "Started", "Keyboard blocking has started.")

        else:

            if self.keyboard_blocker is not None:

                self.keyboard_blocker.unhook()
                self.keyboard_blocker = None
                self.blocking_thread = None
                QMessageBox.information(self, "Stopped", "Keyboard blocking has stopped.")

    def disable_keyboard(self):

        self.keyboard_blocker = KeyboardBlocker()
        self.blocking_thread = threading.Thread(target=self.keyboard_blocker.start)
        self.blocking_thread.daemon = True  # Allows the thread to close when the main program exits
        self.blocking_thread.start()
        QMessageBox.information(self, "Started", "Keyboard blocking has started.")
        pass
    
    def enable_keyboard(self):

        if self.keyboard_blocker is not None:
            self.keyboard_blocker.unhook()
            self.keyboard_blocker = None
            self.blocking_thread = None
            QMessageBox.information(self, "Stopped", "Keyboard blocking has stopped.")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = KeyLockerApp()
    window.show()
    sys.exit(app.exec_())