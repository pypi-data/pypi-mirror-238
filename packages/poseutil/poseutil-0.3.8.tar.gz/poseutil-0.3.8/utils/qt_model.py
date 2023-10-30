from PyQt6.QtWidgets import QMainWindow, QDialog
from PyQt6. QtGui import QGuiApplication
from PyQt6 import QtCore
from enum import Enum
import threading


class AppMode(Enum):
    normal = 1
    debug = 2

class BaseQMainWindow(QMainWindow):
    def __init__(self, width, height, mode):
        super().__init__()
        self.mode = mode
        if mode == AppMode.normal:
            self.monitor = QGuiApplication.screens()[0].geometry()
        elif mode == AppMode.debug:
            if len(QGuiApplication.screens()) > 1:
                self.monitor = QGuiApplication.screens()[2].geometry()
            elif len(QGuiApplication.screens()) > 0:
                self.monitor = QGuiApplication.screens()[1].geometry()
            else :
                self.monitor = QGuiApplication.screens()[0].geometry()
        self.setGeometry(self.monitor.left(), self.monitor.top(), width, height)
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key.Key_Escape:
            self.close()

class BaseQDialog(QDialog):
    def __init__(self, width, height, mode):
        super().__init__()
        self.mode = mode
        if mode == AppMode.normal:
            self.monitor = QGuiApplication.primaryScreen().availableGeometry()
        elif mode == AppMode.debug:
            self.monitor = QGuiApplication.primaryScreen().availableGeometry()
        self.setGeometry(self.monitor.left(), self.monitor.top(), width, height)

class StoppableThread(threading.Thread):
    
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()