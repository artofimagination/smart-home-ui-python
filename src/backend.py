from PyQt5.QtCore import QObject, QThread
from PyQt5 import QtCore

import traceback
import sys


# Signals used by the backend.
class BackendSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)


class Backend(QObject):
    """! Backend logic to handle the business logic.
    """

    def __init__(self):
        super(Backend, self).__init__()
        self.signals = BackendSignals()

        # Thread break guard condition, when true the thread finishes.
        self.stop = False

    @QtCore.pyqtSlot()
    def run(self):
        """
            Main loop of the backend.
        """
        try:
            print("Backend")
            while (True):
                QThread.msleep(10)
                # Backend stopped. Exit.
                if self.stop:
                    break

        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()  # Done
