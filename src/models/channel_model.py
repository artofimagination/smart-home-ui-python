from PyQt5.QtGui import QColor


class ChannelModel():
    """Data model for the channel gui item"""
    def __init__(self):
        self.animation_speed = 1
        self.arrow_density = 1
        self.text = "--"
        self.channel_color = QColor(0, 255, 0, 200)
        self.arrow_color = QColor(0, 0, 255, 200)
        self.arrows_reversed = False
