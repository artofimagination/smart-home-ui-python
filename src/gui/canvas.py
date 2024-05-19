from PyQt5 import QtWidgets, QtGui, QtCore

from gui.channel import Channel
from gui.component_gui import ComponentGui

from helper_defs import (
    TYPE_SOLAR_PANEL,
    TYPE_BATTERY
)


class CustomScene(QtWidgets.QGraphicsScene):
    """ Custom scene to handle special background"""
    def __init__(self, background_image_path, parent=None):
        super().__init__(parent)
        self.background_image = QtGui.QPixmap(background_image_path)

    def drawBackground(self, painter, rect):
        """
        Draw a centered background image within the given rect.
        The rest of the scene will be black.
        """
        if not self.background_image.isNull():
            # Get the size of the current scene view rect
            scene_rect = self.sceneRect()
            painter.fillRect(rect, QtGui.QColor("#010101"))

            # Calculate the position to center the image
            image_width = self.background_image.width()
            image_height = self.background_image.height()
            x = (scene_rect.width() - image_width) / 2
            y = (scene_rect.height() - image_height) / 2

            # Draw the pixmap at the calculated position
            painter.drawPixmap(QtCore.QPointF(x, y), self.background_image)


class Canvas(QtWidgets.QGraphicsView):
    """Custom canvas to plot the smart home ui."""
    def __init__(self):
        super().__init__()
        self.scene = CustomScene("src/resources/canvas_bg.jpg")
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("#111111")))
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)
        self.component_list = list()
        self.channels = list()

    def add_new_component_gui(self, id: int, type: int, x: int, y: int):
        """
            Creates a new component gui based on the input type and attaches it to
            the backend component via its id.

            Parameters:
                - id (int): Id of the component the gui item will be created for
                - type (int): type of the gui item
                - x (int): x coordinate where the gui item expected to be created at
                - y (int): y coordinate where the gui item expected to be created at
        """
        if type == TYPE_SOLAR_PANEL:
            self.component_list.append(ComponentGui(id, self.scene, x, y, "src/resources/solar_panel_icon.png"))
        elif type == TYPE_BATTERY:
            self.component_list.append(ComponentGui(id, self.scene, x, y, "src/resources/battery_icon.png"))
        else:
            raise Exception("Unknown component id")

        if len(self.component_list) - 1 != id:
            raise Exception("GUI and backend component id mismatch")

    def add_new_channel(self, id_start, id_end):
        """
            Adds a new channel between the start and end component
            defined by \a id_start and \a id_end.
        """
        channel = Channel(
            id_start,
            id_end,
            self.component_list[id_start].rect(),
            self.component_list[id_end].rect(),
            self.scene)
        channel.draw()
        self.channels.append(channel)
