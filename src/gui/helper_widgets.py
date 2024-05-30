from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QSpacerItem,
    QWidgetItem
)

from PyQt5.QtCore import (
    Qt
)

from PyQt5.QtGui import (
    QPainter,
    QPen,
    QColor
)


class GridContainer(QWidget):
    """
        Custom grid layout, that allows to draw debug rectangles and custom styled layout.
    """
    def __init__(self, parent=None):
        super(GridContainer, self).__init__(parent)
        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)
        self.draw_rect = False

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#EE202020"))
        painter.setPen(QColor("#FF202020"))
        corner_radius = 10
        painter.drawRoundedRect(self.rect(), corner_radius, corner_radius)
        pen_width = 10
        painter.setPen(QColor("#EEAAAAAA"))
        painter.setBrush(Qt.NoBrush)

        # Draw a rounded border rectangle
        border_rect = self.rect().adjusted(pen_width, pen_width, -pen_width, -pen_width)
        painter.drawRoundedRect(border_rect, corner_radius, corner_radius)
        if self.draw_rect is False:
            return
        painter.setPen(QPen(QColor(100, 100, 100), 2))

        for row in range(self.grid_layout.rowCount()):
            for col in range(self.grid_layout.columnCount()):
                painter.setPen(QPen(QColor(100, 100, 100), 2))
                rect = self.grid_layout.cellRect(row, col)
                painter.drawRect(rect)
                item = self.grid_layout.itemAtPosition(row, col)
                if item:
                    if isinstance(item, QWidgetItem):
                        rect = item.widget().geometry()
                    elif isinstance(item, QSpacerItem):
                        painter.setPen(QPen(QColor(200, 200, 200), 2))
                        rect = self.grid_layout.cellRect(row, col)
                    painter.drawRect(rect)


class BorderedButton(QPushButton):
    """
        Custom button to allow optional debug rectangles around the button.
    """
    def __init__(self, title, parent=None):
        super(BorderedButton, self).__init__(title, parent)
        self.draw_rect = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.draw_rect is False:
            return
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 0, 0), 2))  # Red border with 2px width
        painter.drawRect(self.rect())
