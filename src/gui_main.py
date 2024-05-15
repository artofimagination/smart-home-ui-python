from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
)

from PyQt5.QtCore import QThread

from backend import Backend
from gui.canvas import Canvas


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
        self.setCentralWidget(self.create_canvas_layout())

        self.worker.moveToThread(self.workerThread)
        self.workerThread.finished.connect(self.worker.deleteLater)
        self.workerThread.started.connect(self.worker.run)
        self.workerThread.start()
        self.show()

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
