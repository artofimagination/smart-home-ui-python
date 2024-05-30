from PyQt5.QtGui import (
    QPixmap
)

TYPE_SOLAR_PANEL = 0
TYPE_BATTERY = 1


def invert_colors(pixmap):
    """ Inverts the colors of the given QPixmap. """
    image = pixmap.toImage()  # Convert QPixmap to QImage for manipulation
    image.invertPixels()  # Invert all pixel colors
    return QPixmap.fromImage(image)
