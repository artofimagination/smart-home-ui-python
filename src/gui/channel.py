from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, QTimer

from PyQt5.QtCore import (
    QPointF
)

import math


class Arrowhead(QtWidgets.QGraphicsPolygonItem):
    def __init__(self, size=10, segment_index=0, parent=None):
        super().__init__(parent)
        self.size = size
        self.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 200), 1))
        self.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 255, 200)))
        self.segment_index = segment_index

        # Create the arrowhead shape
        triangle = QtGui.QPolygonF([
            QPointF(0, 0),
            QPointF(-size / 3, -size / 2),
            QPointF(-size, -size / 2),
            QPointF(-2 * size / 3, 0),
            QPointF(-size, size / 2),
            QPointF(-size / 3, size / 2),
        ])
        self.setPolygon(triangle)


class Channel(QObject):
    """
    Channel is a directional wire connecting two components. The channel can have two segments,
    depending on if the two components x, y coordinates. The wire has animated arrows moving towards
    the direction of the flow.
    """
    DIRECTION_RIGHT = 1     # Channel segment left direction
    DIRECTION_TOP = 2       # Channel segment top direction
    DIRECTION_LEFT = 3      # Channel segment left direction
    DIRECTION_BOTTOM = 4    # Channel segment bottom direction

    def __init__(self, start_rect, end_rect, scene):
        super(Channel, self).__init__()
        self.scene = scene
        self.arrow_density = 20
        self.animation_speed = 5  # Speed in pixels per frame
        self.text_item = QtWidgets.QGraphicsTextItem("3 kWh")
        self.text_item.setDefaultTextColor(QtGui.QColor('lightgray'))
        self.text_item.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.scene.addItem(self.text_item)

        # Prepare the error animation
        self.error_animation = QtCore.QPropertyAnimation(self.text_item, b"opacity")
        self.error_animation.setDuration(1000)
        self.error_animation.setLoopCount(-1)  # Infinite loop
        self.error_animation.setKeyValueAt(0, 0)
        self.error_animation.setKeyValueAt(0.5, 1)
        self.error_animation.setKeyValueAt(1, 0)

        # Calculate closest edge points and corner
        self.start_edge_point, self.corner_point, self.end_edge_point = self._get_connecting_edge_points(
            start_rect, end_rect
        )
        self._set_text_position()

        # Initialize the arrows
        self.arrowheads = self.create_arrows(self.start_edge_point, self.end_edge_point, num_arrows=self.arrow_density)
        self.direction_vector = QPointF(
            self.end_edge_point.x() - self.start_edge_point.x(),
            self.end_edge_point.y() - self.start_edge_point.y()
        )
        length = math.sqrt(self.direction_vector.x() ** 2 + self.direction_vector.y() ** 2)

        if length != 0:
            # Normalize direction vector
            self.direction_vector /= length

        # Set up arrows animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_arrows)
        self.timer.start(100)

    def _set_text_position(self):
        """
        Sets the text position on the horizontal part of the channel.
        It is always set on the side, further away from the farther component.
        """
        if self.start_edge_point.y() == self.corner_point.y():
            self.text_item.setPos(
                int((self.start_edge_point.x() - self.corner_point.x()) / 2) + self.corner_point.x(),
                self.start_edge_point.y() - 30)
            if self.end_edge_point.y() < self.start_edge_point.y():
                self.text_item.setPos(
                    int((self.start_edge_point.x() - self.corner_point.x()) / 2) + self.corner_point.x(),
                    self.start_edge_point.y() + 30)
        elif self.end_edge_point.y() == self.corner_point.y():
            self.text_item.setPos(
                int((self.end_edge_point.x() - self.corner_point.x()) / 2) + self.corner_point.x(),
                self.end_edge_point.y() - 30)
            if self.end_edge_point.y() < self.start_edge_point.y():
                self.text_item.setPos(
                    int((self.end_edge_point.x() - self.corner_point.x()) / 2) + self.corner_point.x(),
                    self.end_edge_point.y() - 30)

    def triggerError(self, error=True):
        """ Trigger or clear an error state. """
        if error:
            self.text_item.setDefaultTextColor(QtGui.QColor(200, 0, 0, 150))
            self.text_item.setPlainText("0.5 kWh")
            self.error_animation.start()
        else:
            self.error_animation.stop()
            self.text_item.setOpacity(1)  # Ensure full visibility
            self.text_item.setDefaultTextColor(QtGui.QColor(200, 200, 200, 150))
            self.text_item.setPlainText("5 kWh")

    def _get_connecting_edge_points(self, rect1, rect2):
        """Get the connecting edge points between two icon bounding rectangles."""
        center1 = rect1.center()
        center2 = rect2.center()

        # Determine directions
        delta_x = center2.x() - center1.x()
        delta_y = center2.y() - center1.y()

        # Compute which edge of rect1 is closest to rect2
        if abs(delta_x) > abs(delta_y):
            start_x = rect1.right() if delta_x > 0 else rect1.left()
            start_y = center1.y()
        else:
            start_y = rect1.bottom() if delta_y > 0 else rect1.top()
            start_x = center1.x()

        # Compute which edge of rect2 is closest to rect1
        if abs(delta_x) > abs(delta_y):
            if delta_y == 0:
                end_x = rect2.right() if delta_x < 0 else rect2.left()
                end_y = center2.y()
            else:
                end_x = center2.x() if delta_x < 0 else center2.x()
                end_y = rect2.left()
        else:
            if delta_x == 0:
                end_y = rect2.bottom() if delta_y < 0 else rect2.top()
                end_x = center2.x()
            else:
                end_y = center2.y()
                end_x = rect2.right() if delta_x < 0 else rect2.left()

        corner = QPointF(start_x, end_y)
        if start_x == end_x:
            corner = QPointF(start_x, (start_y + end_y) / 2)
        elif start_y == end_y:
            corner = QPointF((start_x + end_x) / 2, end_y)

        return QPointF(start_x, start_y), corner, QPointF(end_x, end_y)

    def create_arrows(self, start_point: QPointF, end_point: QPointF, num_arrows: int) -> list:
        """
            Create and position arrows along the path.

            Parameters:
                - start_point (QPointF): start point of the segment the arrow is placed.
                - end_point (QPointF): end point of the segment the arrow is placed.
                - num_arrows: (int): number of arrows to be placed.

            Returns:
                List of created arrows
        """
        arrowheads = list()
        start_segment_direction = self._get_direction(self.start_edge_point, self.corner_point)
        end_segment_direction = self._get_direction(self.corner_point, self.end_edge_point)
        dx = self.corner_point.x() - start_point.x()
        dy = self.corner_point.y() - start_point.y()

        num_arrows = int(num_arrows / 2)
        step_x = dx / num_arrows
        step_y = dy / num_arrows

        for i in range(num_arrows):
            arrowhead = Arrowhead(size=7, segment_index=0)
            position = QPointF(start_point.x() + step_x * i, start_point.y() + step_y * i)

            # Calculate angle and rotate arrowhead to follow the path direction
            arrowhead.setRotation(self._get_rotation(start_segment_direction))
            arrowhead.setPos(position)

            self.scene.addItem(arrowhead)
            arrowheads.append(arrowhead)

        dx = end_point.x() - self.corner_point.x()
        dy = end_point.y() - self.corner_point.y()

        step_x = dx / num_arrows
        step_y = dy / num_arrows

        for i in range(num_arrows):
            arrowhead = Arrowhead(size=7, segment_index=1)
            position = QPointF(self.corner_point.x() + step_x * i, self.corner_point.y() + step_y * i)

            # Calculate angle and rotate arrowhead to follow the path direction
            arrowhead.setRotation(self._get_rotation(end_segment_direction))
            arrowhead.setPos(position)

            self.scene.addItem(arrowhead)
            arrowheads.append(arrowhead)

        return arrowheads

    def _draw_channel(self):
        """
            Draw a channel (tube) between two graphical items,
            with a black outline and gradient filling parallel to the path.
        """

        # Create the path for the tube
        path = QtGui.QPainterPath()
        path.moveTo(self.start_edge_point)
        path.lineTo(self.corner_point)
        path.lineTo(self.end_edge_point)

        # Draw the black outer outline by creating a separate outer path
        outline_path = QtGui.QPainterPath()
        outline_path.addPath(path)

        outer_pen = QtGui.QPen(QtGui.QColor(100, 100, 100), 11)  # Wider than inner path to create a border
        outer_pen.setJoinStyle(QtCore.Qt.MiterJoin)
        outline = QtWidgets.QGraphicsPathItem()
        outline.setPath(outline_path)
        outline.setPen(outer_pen)
        outline.setBrush(QtGui.QBrush(QtCore.Qt.NoBrush))
        outline.setZValue(-2)
        self.scene.addItem(outline)

        direction_start = self._get_direction(self.start_edge_point, self.corner_point)
        direction_end = self._get_direction(self.corner_point, self.end_edge_point)
        if (direction_start != direction_end):
            if direction_start == self.DIRECTION_TOP and direction_end == self.DIRECTION_LEFT:
                triangle_path1 = QtGui.QPainterPath()
                triangle_path1.moveTo(QPointF(self.corner_point.x() - 1.0, self.corner_point.y() + 2.0))  # left
                triangle_path1.lineTo(QPointF(self.corner_point.x() + 2.0, self.corner_point.y() + 2.0))  # bottom-right
                triangle_path1.lineTo(QPointF(self.corner_point.x() + 2.0, self.corner_point.y()))        # top
                triangle_path1.lineTo(QPointF(self.corner_point.x() - 1.0, self.corner_point.y() + 2.0))  # left
                path.closeSubpath()
            elif direction_start == self.DIRECTION_BOTTOM and direction_end == self.DIRECTION_RIGHT:
                triangle_path1 = QtGui.QPainterPath()
                triangle_path1.moveTo(QPointF(self.corner_point.x() - 2.0, self.corner_point.y()))  # left
                triangle_path1.lineTo(QPointF(self.corner_point.x() - 2.0, self.corner_point.y() - 3.0))  # top-left
                triangle_path1.lineTo(QPointF(self.corner_point.x() + 1.0, self.corner_point.y() - 3.0))  # top-right
                triangle_path1.lineTo(QPointF(self.corner_point.x() - 2.0, self.corner_point.y()))  # left
                path.closeSubpath()
            elif direction_start == self.DIRECTION_TOP and direction_end == self.DIRECTION_RIGHT:
                triangle_path1 = QtGui.QPainterPath()
                triangle_path1.moveTo(QPointF(self.corner_point.x() - 2.0, self.corner_point.y() + 2.0))  # left
                triangle_path1.lineTo(QPointF(self.corner_point.x() - 2.0, self.corner_point.y()))  # top-left
                triangle_path1.lineTo(QPointF(self.corner_point.x() + 1.0, self.corner_point.y() + 2.0))  # top-right
                triangle_path1.lineTo(QPointF(self.corner_point.x() - 2.0, self.corner_point.y() + 2.0))  # left
                path.closeSubpath()
            else:
                triangle_path1 = QtGui.QPainterPath()
                triangle_path1.moveTo(QPointF(self.corner_point.x() + 2.0, self.corner_point.y()))  # left
                triangle_path1.lineTo(QPointF(self.corner_point.x() - 1.0, self.corner_point.y() - 3.0))  # top-left
                triangle_path1.lineTo(QPointF(self.corner_point.x() + 2.0, self.corner_point.y() - 3.0))  # top-right
                triangle_path1.lineTo(QPointF(self.corner_point.x() + 2.0, self.corner_point.y()))  # left               

        # Calculate gradients for each channel turn permutation.
        gradient_start = self.start_edge_point
        gradient_end = QPointF(self.start_edge_point.x(), self.start_edge_point.y() + 6)
        end_gradient_offset = 6
        if (direction_start == self.DIRECTION_BOTTOM and direction_end == self.DIRECTION_LEFT) or \
                (direction_start == self.DIRECTION_TOP and direction_end == self.DIRECTION_RIGHT):
            end_gradient_offset = -6

        if direction_start == self.DIRECTION_TOP or direction_start == self.DIRECTION_BOTTOM:
            gradient_start = self.start_edge_point
            gradient_end = QPointF(self.start_edge_point.x() - 6, self.start_edge_point.y())

        gradient1 = QtGui.QLinearGradient(gradient_start, gradient_end)
        gradient1.setColorAt(0, QtGui.QColor('green'))
        gradient1.setColorAt(1, QtGui.QColor('white'))

        # Second segment
        if direction_end == self.DIRECTION_TOP or direction_end == self.DIRECTION_BOTTOM:
            gradient_start = self.corner_point
            gradient_end = QPointF(self.corner_point.x() - 6, self.corner_point.y())
        else:
            gradient_start = self.corner_point
            gradient_end = QPointF(self.corner_point.x(), self.corner_point.y() + end_gradient_offset)
        gradient2 = QtGui.QLinearGradient(gradient_start, gradient_end)
        gradient2.setColorAt(0, QtGui.QColor('green'))
        gradient2.setColorAt(1, QtGui.QColor('white'))

        gradient_start = self.start_edge_point
        gradient_end = QPointF(self.start_edge_point.x() - 6, self.start_edge_point.y())
        gradient3 = QtGui.QLinearGradient(gradient_start, gradient_end)
        gradient3.setColorAt(0, QtGui.QColor('green'))
        gradient3.setColorAt(1, QtGui.QColor('white'))

        # Create pens for each segment with respective gradients
        inner_pen1 = QtGui.QPen(gradient1, 8)
        inner_pen1.setJoinStyle(QtCore.Qt.MiterJoin)
        inner_pen2 = QtGui.QPen(gradient2, 8)
        inner_pen2.setJoinStyle(QtCore.Qt.MiterJoin)

        # Draw the gradient filling as an inner path with two parts
        fill_path1 = QtGui.QPainterPath()
        fill_path1.moveTo(self.start_edge_point)
        fill_path1.lineTo(self.corner_point)

        fill_path2 = QtGui.QPainterPath()
        fill_path2.moveTo(self.corner_point)
        fill_path2.lineTo(self.end_edge_point)

        fill1 = QtWidgets.QGraphicsPathItem()
        fill1.setPath(fill_path1)
        fill1.setPen(inner_pen1)
        fill1.setZValue(-1)
        self.scene.addItem(fill1)

        fill2 = QtWidgets.QGraphicsPathItem()
        fill2.setPath(fill_path2)
        fill2.setPen(inner_pen2)
        fill2.setZValue(-1)
        self.scene.addItem(fill2)

        if (direction_start != direction_end):
            inner_pen3 = QtGui.QPen(gradient3, 4)
            inner_pen3.setJoinStyle(QtCore.Qt.MiterJoin)
            triangle_fill1 = QtWidgets.QGraphicsPathItem(triangle_path1)
            triangle_fill1.setPen(inner_pen3)
            triangle_fill1.setZValue(-1)
            self.scene.addItem(triangle_fill1)

    def _get_movement_rate(self, direction: int) -> QPointF:
        """Returns the directional movement rate in a from of a 2D point."""
        if direction == self.DIRECTION_RIGHT:
            return QPointF(self.animation_speed, 0)
        elif direction == self.DIRECTION_LEFT:
            return QPointF(-self.animation_speed, 0)
        elif direction == self.DIRECTION_TOP:
            return QPointF(0, -self.animation_speed)
        elif direction == self.DIRECTION_BOTTOM:
            return QPointF(0, self.animation_speed)

    def _segment_end_reached(
            self,
            start: QPointF,
            end: QPointF,
            direction: int,
            rate: QPointF) -> bool:
        """
        Returns true if the segment end is reached.

        Parameters:
            - start (QPointF): start point of the segment.
            - end (QPointF): end point of the segment.
            - direction (int): direction in which the segment points (left, right, top, bottom)
            - rate (QPointF): animation rate of the arrow movement stored in a 2D coordinate.

        Returns:
            True if the end of the segment is reached.
        """
        if direction == self.DIRECTION_RIGHT and (start + rate).x() > end.x():
            return True
        elif direction == self.DIRECTION_LEFT and (start + rate).x() < end.x():
            return True
        elif direction == self.DIRECTION_TOP and (start + rate).y() < end.y():
            return True
        elif direction == self.DIRECTION_BOTTOM and (start + rate).y() > end.y():
            return True
        return False

    def _get_direction(self, start, end) -> int:
        """Returns the direction of the segment."""
        if start.y() == end.y() and start.x() < end.x():
            return self.DIRECTION_RIGHT
        elif start.y() == end.y() and start.x() > end.x():
            return self.DIRECTION_LEFT
        elif start.x() == end.x() and start.y() < end.y():
            return self.DIRECTION_BOTTOM
        else:
            return self.DIRECTION_TOP

    def _get_rotation(self, direction: int) -> int:
        """
        Returns the rotation angle based on the direction

        Parameters:
            - direction (int): Direction in which the rotation shall happen
        Returns:
            The rotation angle
        """
        angle = 0
        if direction == self.DIRECTION_RIGHT:
            angle = 0
        elif direction == self.DIRECTION_LEFT:
            angle = 180
        elif direction == self.DIRECTION_TOP:
            angle = -90
        elif direction == self.DIRECTION_BOTTOM:
            angle = 90
        return angle

    def animate_arrows(self):
        """Animate the arrowheads to simulate flow through an L-shaped channel."""
        for arrow in self.arrowheads:
            current_pos = arrow.pos()
            start_segment_direction = self._get_direction(self.start_edge_point, self.corner_point)
            end_segment_direction = self._get_direction(self.corner_point, self.end_edge_point)
            start_segment_rate = self._get_movement_rate(start_segment_direction)
            end_segment_rate = self._get_movement_rate(end_segment_direction)
            rate = start_segment_rate
            if self._segment_end_reached(
               current_pos, self.corner_point, start_segment_direction, start_segment_rate):
                rate = end_segment_rate
                arrow.setRotation(self._get_rotation(end_segment_direction))
                if arrow.segment_index == 0:
                    current_pos = self.corner_point
                    arrow.segment_index = 1

                if self._segment_end_reached(
                        current_pos, self.end_edge_point, end_segment_direction, end_segment_rate):
                    arrow.setPos(self.start_edge_point)
                    current_pos = arrow.pos()
                    arrow.setRotation(self._get_rotation(start_segment_direction))
                    rate = start_segment_rate
                    arrow.segment_index = 0

            next_pos = current_pos + rate
            arrow.setPos(next_pos)
