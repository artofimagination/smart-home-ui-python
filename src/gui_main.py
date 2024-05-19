from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
)

from PyQt5.QtCore import QThread, QTimer

from backend import Backend
from gui.canvas import Canvas
from models.model_updater import ModelUpdater

from helper_defs import (
    TYPE_SOLAR_PANEL,
    TYPE_BATTERY
)


# Main Qt UI window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.workerThread = QThread(self)
        self.worker = Backend()
        self.worker.signals.error.connect(self.sigint_handler)
        self.worker.signals.finished.connect(self.thread_complete)

        self.resize(800, 600)
        self.showMaximized()
        self.setWindowTitle("Smart Home")
        self.canvas = self.create_canvas_layout()
        self.create_component(TYPE_SOLAR_PANEL, 0, 0)
        self.create_component(TYPE_BATTERY, 400, 400)
        self.create_connection(0, 1)
        self.worker.update_data()
        self.setCentralWidget(self.canvas)
        self.model_updater = ModelUpdater(self.canvas.component_list, self.canvas.channels, self.worker)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self._update_models)
        self.update_timer.start(1000)

        self.worker.moveToThread(self.workerThread)
        self.workerThread.finished.connect(self.worker.deleteLater)
        self.workerThread.started.connect(self.worker.run)
        self.workerThread.start()
        self.show()

    def create_component(self, type: int, x: int, y: int):
        """
            Creates a new backend and ui component for the appropriate component type.

            Parameters:
                - type (int): component type to create
                - x (int): x coordinate where it was requested to be created at.
                - y (int): y coordinate where it was requested to be created at.
        """
        id = self.worker.electrical_layer_controller.add_component(type)
        self.canvas.add_new_component_gui(id, type, x, y)

    def create_connection(self, id_start: int, id_end: int):
        """
            Creates a connection between two components.

            Parameters:
                - id_start (int): id of the start component.
                - id_end (int): id of the end component.
        """
        self.worker.electrical_layer_controller.add_component_pair(id_start, id_end)
        self.canvas.add_new_channel(id_start, id_end)

    def _update_models(self):
        """Periodicallay called method to update gui data models."""
        self.model_updater.update_component_models()

    def create_canvas_layout(self):
        """Create the main canvas interface."""
        return Canvas()

    def closeEvent(self, event):
        """Override of QMainWindow.closeEvent"""
        # Call the function you want before closing
        self.sigint_handler()

    def sigint_handler(self):
        """Terminate UI and the threads appropriately."""
        if self.worker is not None:
            self.worker.stop = True
            self.workerThread.quit()
            self.workerThread.wait()
        print("Exiting app through GUI")
        QApplication.quit()

    def thread_complete(self):
        """Post action once the thread is completed."""
        print("Worker thread stopped...")
