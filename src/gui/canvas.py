from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication
)

from gui.channel import Channel
from gui.component import Component


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
    def __init__(self):
        super().__init__()
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        self.scene = CustomScene("src/resources/canvas_bg.jpg")
        self.scene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("#111111")))
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)

        # Simulate an error to demonstrate animation
        self.component1 = Component(self.scene, 0, 0, "src/resources/solar_panel_icon.png")
        self.component2 = Component(self.scene, -400, 400, "src/resources/battery_icon.png")

        # Draw a thick wire between the two icons
        self.channel = Channel(self.component1.rect(), self.component2.rect(), self.scene)
        self.channel._draw_channel()
        self.channel.triggerError(False)
