from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QVBoxLayout,
    QWidget,
    QDesktopWidget
)

from PyQt5.QtGui import (
    QIcon,
    QPixmap
)

from PyQt5.QtCore import (
    QSize,
)

from PyQt5.QtCore import QThread, QTimer, Qt

from backend import Backend
from gui.canvas import Canvas
from gui.draggable_option import DraggableButton, Options
from models.model_updater import ModelUpdater

from helper_defs import (
    TYPE_SOLAR_PANEL,
    TYPE_BATTERY,
    invert_colors
)


# Main Qt UI window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.workerThread = QThread(self)
        self.worker = Backend()
        self.worker.signals.error.connect(self.sigint_handler)
        self.worker.signals.finished.connect(self.thread_complete)

        # self.resize(800, 600)
        screen = QDesktopWidget().screenGeometry()
        # Set the window size to match the screen size
        self.setGeometry(screen)
        self.showMaximized()
        self.setWindowTitle("Smart Home")
        self.canvas = self.create_canvas_layout()
        self.create_component(TYPE_SOLAR_PANEL, 0, 0)
        self.create_component(TYPE_BATTERY, 400, 400)
        self.create_connection(0, 1)
        self.worker.update_data()
        self.setCentralWidget(self.canvas)
        main_layout = QVBoxLayout(self.canvas)
        main_layout = self._create_options(main_layout)
        self.model_updater = ModelUpdater(self.canvas.component_list, self.canvas.channels, self.worker)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self._update_models)
        self.update_timer.start(1000)

        self.worker.moveToThread(self.workerThread)
        self.workerThread.finished.connect(self.worker.deleteLater)
        self.workerThread.started.connect(self.worker.run)
        self.workerThread.start()
        self.show()

    def _create_options(self, main_layout):
        """
            Creates the dropdown options menu.
        """
        draggable_option_container = QWidget(self)
        draggable_option_container.setGeometry(0, 0, self.width(), self.height())
        draggable_option_container_layout = QVBoxLayout()
        draggable_option_container.setLayout(draggable_option_container_layout)
        self.options_widget = Options(draggable_option_container)
        self.arrow_button = DraggableButton(
            "",
            self.options_widget.open_options_widget,
            self.options_widget.move_options_widget,
            self.options_widget.release_options_widget,
            draggable_option_container)
        self.options_widget.back_button.pressed.connect(self.arrow_button.animate_back)
        pixmap = QPixmap("src/resources/down_arrow.png")
        pixmap = invert_colors(pixmap)
        self.arrow_button.setIcon(QIcon(pixmap))
        self.arrow_button.setIconSize(QSize(64, 20))
        self.arrow_button.setMouseTracking(True)
        main_layout.setContentsMargins(0, 0, 0, 0)
        draggable_option_container_layout.addWidget(self.options_widget, 0, Qt.AlignCenter)
        draggable_option_container_layout.addWidget(self.arrow_button, 0, Qt.AlignCenter)
        main_layout.addWidget(draggable_option_container, 0)
        return main_layout

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
