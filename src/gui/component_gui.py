from PyQt5.QtCore import QObject, QRect, QPointF
from PyQt5.QtGui import QTransform

import pyqtgraph as pg

from gui.icon import AnimatedIcon
from models.component_model import ComponentModel


class ComponentGui(QObject):
    """
        A component defines an icon and belonging chart.
    """
    def __init__(self, component_id, scene, x, y, image_path):
        self.component_id = component_id
        self.scene = scene
        self.model = ComponentModel()
        self.model.main_icon_path = image_path
        self.model.component_location = QPointF(x, y)
        self.plot = None
        self.icon = self._create_icon(x, y, 128, 128)
        self.graph = self._create_graph(x + 120, y - 80)

    def rect(self) -> QRect:
        """Returns the component gui element bounding rectangle."""
        return self.icon.sceneBoundingRect()

    def _create_icon(self, x, y, width, height):
        """Add an icon image to the canvas at the specified coordinates."""
        icon = AnimatedIcon(self.model.main_icon_path, width, height)
        icon.text = self.model.main_icon_data
        icon.setPos(x, y)
        self.scene.addItem(icon)
        # icon.trigger_error()
        return icon

    def _create_graph(self, x, y):
        """ Add a pyqtgraph plot to the scene. """
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', (0, 0, 0, 0))
        graph_widget = pg.GraphicsLayoutWidget()
        graph_widget.setStyleSheet("GraphicsLayoutWidget { background-color: rgba(255, 255, 255, 30); }")
        self.plot = graph_widget.addPlot()
        self.plot.plot(self.model.thumbnail_chart_timestamp, self.model.thumbnail_chart_data1)  # Example data
        self.plot.getViewBox().setBackgroundColor((0, 0, 0, 0))

        # Convert the GraphicsLayoutWidget to a QGraphicsProxyWidget
        proxy_widget = self.scene.addWidget(graph_widget)
        proxy_widget.setPos(x, y)  # Position the graph in the scene
        proxy_widget.setTransform(QTransform().scale(0.2, 0.2))
        return proxy_widget

    def update_component(self):
        """Updates the component gui via the data model."""
        self.icon.setPos(self.model.component_location.x(), self.model.component_location.y())
        self.icon.text = self.model.main_icon_data
        self.graph.setPos(self.model.component_location.x() + 120, self.model.component_location.y() - 80)
        self.plot.clear()
        self.plot.plot(self.model.thumbnail_chart_timestamp, self.model.thumbnail_chart_data1)
        self.icon.update()
