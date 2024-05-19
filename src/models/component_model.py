from PyQt5.QtCore import QPointF


class ComponentModel():
    """Data model for component Gui items."""
    STATE_OK = 0
    STATE_ERROR = 1

    def __init__(self):
        self.main_icon_data = None
        self.main_icon_state = self.STATE_OK
        self.main_icon_path = ""
        self.component_location = QPointF()
        self.thumbnail_chart_data1 = list()
        self.thumbnail_chart_data2 = None
        self.thumbnail_chart_area1 = None
        self.thumbnail_chart_area2 = None
        self.thumbnail_chart_timestamp = list()
