from PyQt5.QtCore import QObject, QRect
from PyQt5.QtGui import QTransform

import pyqtgraph as pg

from gui.icon import AnimatedIcon


class Component(QObject):
    """
        A component defines an icon and belonging chart.
    """
    def __init__(self, scene, x, y, image_path):
        self.scene = scene
        self.icon = self._create_icon(x, y, image_path, 128, 128)
        self.graph = self._create_graph(x + 120, y - 80)

    def rect(self) -> QRect:
        return self.icon.sceneBoundingRect()

    def _create_icon(self, x, y, icon_path, width, height):
        """Add an icon image to the canvas at the specified coordinates."""
        pixmap = AnimatedIcon(icon_path, width, height)
        pixmap.setPos(x, y)
        self.scene.addItem(pixmap)
        pixmap.trigger_error()
        return pixmap

    def _create_graph(self, x, y):
        """ Add a pyqtgraph plot to the scene. """
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', (0, 0, 0, 0))
        graph_widget = pg.GraphicsLayoutWidget()
        graph_widget.setStyleSheet("GraphicsLayoutWidget { background-color: rgba(255, 255, 255, 30); }")
        plot = graph_widget.addPlot(title="Sample Plot")
        plot.plot([1, 2, 3, 4, 5], [5, 3, 9, 1, 6])  # Example data
        plot.getViewBox().setBackgroundColor((0, 0, 0, 0))

        # Convert the GraphicsLayoutWidget to a QGraphicsProxyWidget
        proxy_widget = self.scene.addWidget(graph_widget)
        proxy_widget.setPos(x, y)  # Position the graph in the scene
        proxy_widget.setTransform(QTransform().scale(0.2, 0.2))
