from PyQt5.QtCore import QObject, QThread, QTimer, QCoreApplication
from PyQt5 import QtCore

import traceback
import sys

from layer_controller import LayerController


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
        self.electrical_layer_controller = LayerController()

        # Thread break guard condition, when true the thread finishes.
        self.stop = False
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(1000)

    def update_data(self):
        """
            Periodically called method to update layer controller and all
            underlying component controllers.
        """
        self.electrical_layer_controller.update_demo()

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
                QCoreApplication.processEvents()

        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()  # Done
