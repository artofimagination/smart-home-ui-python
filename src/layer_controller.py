from helper_defs import (
    TYPE_SOLAR_PANEL,
    TYPE_BATTERY
)
from components.solar_controller import SolarController
from components.battery_controller import BatteryController


class LayerController():
    """
        Generic class to handle layers of the smart home layout.
        Layers can be, heat flow, electrical flow, heat mapped floor plan etc.
    """
    def __init__(self):
        self.components = list()
        self.component_pairs = list()

    def add_component(self, type: int) -> int:
        """Creates a new backend component and returns its id in the list."""
        if type == TYPE_SOLAR_PANEL:
            self.components.append(SolarController())
        elif type == TYPE_BATTERY:
            self.components.append(BatteryController())
        else:
            raise Exception("Unknown component type")

        return len(self.components) - 1

    def add_component_pair(self, id_start: int, id_end: int):
        """
            Connects two backend items. Each item will maintain the list of connected id-s

            Parameters
        """
        if id_start >= len(self.components) or id_end >= len(self.components):
            raise Exception("Invalid component id")
        self.components[id_start].connected_ids.append(id_end)
        self.components[id_end].connected_ids.append(id_start)
        self.component_pairs.append((self.components[id_start], self.components[id_end]))

    def update_demo(self):
        """Updates the data of each controller."""
        for component in self.components:
            component.generate_demo_data()
