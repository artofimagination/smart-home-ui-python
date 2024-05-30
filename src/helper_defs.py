from PyQt5.QtGui import (
    QPixmap
)

from PyQt5.QtCore import (
    QFile,
    QIODevice,
    QTextStream
)

TYPE_SOLAR_PANEL = 0
TYPE_BATTERY = 1


def invert_colors(pixmap):
    """ Inverts the colors of the given QPixmap. """
    image = pixmap.toImage()  # Convert QPixmap to QImage for manipulation
    image.invertPixels()  # Invert all pixel colors
    return QPixmap.fromImage(image)


def get_stylesheet(resource) -> str:
    """
        Returns the stylesheet string from the selected resource file.
    """
    stream = QFile(resource)
    stream.open(QIODevice.ReadOnly)
    return QTextStream(stream).readAll()
