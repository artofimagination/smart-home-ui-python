from PyQt5.QtCore import (
    QPropertyAnimation,
    Qt,
    QPoint,
    QSize
)
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QSpacerItem,
    QWidgetItem
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
    QPainter,
    QPen,
    QColor
)

from helper_defs import invert_colors


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


class Options(GridContainer):
    """
        Class to represent the setup dropdown options.
    """
    def __init__(self, parent=None):
        super(Options, self).__init__(parent)
        add_button = BorderedButton('')
        icon_width = 64
        icon_height = 64
        pixmap = QPixmap("src/resources/add_button.png")
        pixmap = invert_colors(pixmap)
        add_button.setIcon(QIcon(pixmap))
        add_button.setIconSize(QSize(icon_width, icon_height))
        add_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #AAAAAAAA;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #807070AA;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
                border-radius: 10px;
            }
        """)
        connect_button = BorderedButton('')
        pixmap = QPixmap("src/resources/connect_button.png")
        pixmap = invert_colors(pixmap)
        connect_button.setIcon(QIcon(pixmap))
        connect_button.setIconSize(QSize(icon_width, icon_height))
        connect_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #AAAAAAAA;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #807070AA;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
                border-radius: 10px;
            }
        """)
        settings_button = BorderedButton('')
        pixmap = QPixmap("src/resources/settings_button.png")
        pixmap = invert_colors(pixmap)
        settings_button.setIcon(QIcon(pixmap))
        settings_button.setIconSize(QSize(icon_width, icon_height))
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #AAAAAAAA;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #807070AA;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
                border-radius: 10px;
            }
        """)
        self.back_button = BorderedButton('')
        pixmap = QPixmap("src/resources/back_arrow.png")
        pixmap = invert_colors(pixmap)
        self.back_button.setIcon(QIcon(pixmap))
        self.back_button.setIconSize(QSize(int(icon_width), int(icon_height / 2)))
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-top: none;
                border-left: none;
                border-right: none;
                border-bottom: none;
                margin: 0px;
                padding: 0px;
            }
        """)
        self.back_button.pressed.connect(self.release_options_widget)
        c_icon_count_in_column = 2
        c_column_spacer_count = c_icon_count_in_column + 1
        col_loc = c_column_spacer_count + c_icon_count_in_column
        self.grid_layout.addWidget(self.back_button, 0, col_loc, 1, 1)
        self.grid_layout.addWidget(add_button, 1, 1, 1, 1)
        self.grid_layout.addWidget(connect_button, 1, 3, 1, 1)
        self.grid_layout.addWidget(settings_button, 3, 1, 1, 1)
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(500)
        self.setFixedSize(int(parent.width() / 2), int(parent.height() / 3))
        self.original_position = QPoint(int(parent.width() / 2 - self.width() / 2), -self.height())
        self.animation.setStartValue(QPoint(self.original_position.x(), -self.height()))
        self.animation.setEndValue(QPoint(self.original_position.x(), -self.height()))
        self.animation.start()

    def open_options_widget(self):
        """
            Animate options widget to roll down the screen if the drag is more
            than half the screen.
        """
        self.animation.setStartValue(QPoint(self.original_position.x(), self.y()))
        self.animation.setEndValue(QPoint(self.original_position.x(), self.height()))
        self.animation.start()

    def move_options_widget(self, y_pos):
        """
            Animate options widget to fill the screen.
        """
        self.move(self.original_position.x(), -self.height() + y_pos.y())

    def release_options_widget(self):
        """
            Antimate option to move back to original location, when the drag is less than half
            the screen.
        """
        self.animation.setStartValue(QPoint(self.original_position.x(), self.y()))
        self.animation.setEndValue(QPoint(self.original_position.x(), -self.height()))
        self.animation.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.draw_rect is False:
            return
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 0, 255), 2))  # Red border with 2px width
        painter.drawRect(self.rect())


class DraggableButton(BorderedButton):
    def __init__(self, title, open_option, move_option, release_option, parent=None):
        super(DraggableButton, self).__init__(title, parent)
        self.setMouseTracking(True)
        self.mouse_pressed = False
        self.open_option = open_option
        self.release_option = release_option
        self.move_option = move_option
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(500)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-top: none;
                border-bottom: 2px solid gray;
                border-left: 2px solid gray;
                border-right: 2px solid gray;
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
                margin: 0px;
                padding: 0px;
            }
        """)

        self.setFixedSize(int(parent.width() / 4), int(parent.height() / 20))
        self.original_position = QPoint(int(parent.width() / 4 + self.width() / 2), 0)
        self.animate_back()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.original_position.setY(self.pos().y())

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            # Calculate new position
            new_pos = event.globalPos() - self.original_position
            self.move_option(new_pos)
            # Limit the dragging to vertical movements
            self.move(self.x(), new_pos.y())

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False
        if self.y() > self.parent().height() / 2:
            self.open_option()
            self.animate_option_on()
        else:
            self.release_option()
            self.animate_back()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.draw_rect is False:
            return
        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 255, 0), 2))  # Red border with 2px width
        painter.drawRect(self.rect())

    def animate_back(self):
        self.animation.setStartValue(QPoint(self.original_position.x(), self.y()))
        self.animation.setEndValue(QPoint(self.original_position.x(), 0))
        self.animation.start()

    def animate_option_on(self):
        self.animation.setStartValue(QPoint(self.x(), self.y()))
        self.animation.setEndValue(QPoint(self.x(), self.parent().height()))
        self.animation.start()
