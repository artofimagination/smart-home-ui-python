from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import (
    QPixmap,
    QColor,
    QPainter,
    QRadialGradient,
    QBrush,
    QPen,
    QFont
)


class AnimatedIcon(QtWidgets.QGraphicsPixmapItem):
    """
    Animated icon where there is an image icon in the center surrounded by a circle
    and a text written under the icon. The whole icon is blinking in red during error.
    """
    ERROR_COLOR = QColor('red')
    DEFAULT_COLOR = QColor('lightblue')

    def __init__(self, image_path, width, height, parent=None):
        super().__init__(parent)
        self.original_pixmap = QPixmap(image_path)
        self.border_color = self.DEFAULT_COLOR
        self.text = "--"
        self.text_color = self.DEFAULT_COLOR

        # Create an animation for the opacity effect
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.error_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.error_animation.setDuration(1000)
        self.error_animation.setStartValue(1.0)
        self.error_animation.setEndValue(0.1)
        self.error_animation.setKeyValueAt(0.5, 0.1)
        self.error_animation.setKeyValueAt(1.0, 1.0)
        self.error_animation.setLoopCount(2)
        self.width = width
        self.height = height
        self._set_pixmap(self.original_pixmap, width, height)
        self.error_animation.finished.connect(self._on_blink_animation_finished)

    def invert_colors(self, pixmap):
        """ Inverts the colors of the given QPixmap. """
        image = pixmap.toImage()  # Convert QPixmap to QImage for manipulation
        image.invertPixels()  # Invert all pixel colors
        return QPixmap.fromImage(image)

    def _set_pixmap(self, pixmap: QPixmap, width: int, height: int):
        """
        Create a component icon that is containing the icon of the component a circle around it
        and the most dominant parameters describing the component.

        Parameters:
            - pixmap (QPixmap): pixmap to show as icons
            - width (int): width of the animated icon in the scene.
            - height (int): height of the animated icon in the scene.
        """
        # The icon is drawn with black color, so inversion is done (should be done during icon preprocessing instead)
        pixmap = self.invert_colors(pixmap)
        border_width = 80  # Set the width of the border
        # Mask pixmap to draw a circle around the icon
        mask_size = pixmap.size() + QtCore.QSize(border_width * 4, border_width * 4)
        mask = QPixmap(mask_size)
        mask.fill(QtCore.Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRect(mask.rect())
        self.gradient = QRadialGradient(
            mask_size.width() / 2, mask_size.height() / 2, mask_size.width() / 2 + border_width * 0.3)
        self.gradient.setColorAt(1, QtCore.Qt.transparent)
        self.gradient.setColorAt(0, self.border_color)  # Start of the gradient (inside)
        painter.setPen(QPen(QBrush(self.gradient), 100))
        painter.drawEllipse(
            int(border_width / 2),
            int(border_width / 2),
            mask_size.width() - border_width,
            mask_size.height() - border_width)

        # Draw the icon, rescaled position within the circle. Also add a text under the icon.
        masked_pixmap = QPixmap(mask_size)
        pixmap = pixmap.scaled(
            int(pixmap.size().width() / 1.5),
            int(pixmap.size().height() / 1.5),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation)
        masked_pixmap.fill(QtCore.Qt.transparent)
        painter = QPainter(masked_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(
            int(mask_size.width() / 2 - pixmap.size().width() / 2),
            int(mask_size.height() / 2 - pixmap.size().height() / 1.5),
            pixmap)
        painter.drawPixmap(0, 0, mask)
        painter.setFont(QFont("Arial", 80, QFont.Bold))
        painter.setPen(self.text_color)
        text_rect = QtCore.QRect(0, int(mask_size.height() / 2), mask.width(), 300)  # Position the text below the image
        painter.drawText(text_rect, QtCore.Qt.AlignCenter, self.text)
        painter.end()

        # Scale the final icon to the neccessary size.
        self.setPixmap(masked_pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def trigger_error(self):
        """ Trigger error animations. """
        self.text_color = self.ERROR_COLOR
        self.border_color = self.ERROR_COLOR
        self._set_pixmap(self.original_pixmap, self.width, self.height)
        self.error_animation.start()

    def _on_blink_animation_finished(self):
        """ Reset border color to blue when the animation finishes. """
        self.border_color = self.DEFAULT_COLOR
        self.text = "5 kWh"
        self.text_color = QColor('#CCCCCCCC')
        self._set_pixmap(self.original_pixmap, self.width, self.height)
