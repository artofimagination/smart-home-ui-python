from PyQt5.QtGui import QColor

from components.solar_controller import SolarController
from components.battery_controller import BatteryController
from backend import Backend
from gui.component_gui import ComponentGui
from gui.channel import Channel
from components.component import Component


class ModelUpdater():
    """This class is repsonsible to update the data models of the different UI scene items."""
    def __init__(self, component_gui_list: list, channel_gui_list: list, backend: Backend):
        self.component_gui_list = component_gui_list
        self.channel_gui_list = channel_gui_list
        self.backend = backend

    def update_component_models(self):
        """Updates all component gui data models and the data models of the channels inbetween."""
        for component_gui in self.component_gui_list:
            component = self.backend.electrical_layer_controller.components[component_gui.component_id]
            if isinstance(component, SolarController):
                component_gui = self._update_solar_panel_model_data(component, component_gui)
            elif isinstance(component, BatteryController):
                component_gui = self._update_battery_model_data(component, component_gui)

        for channel in self.channel_gui_list:
            component = self.backend.electrical_layer_controller.components[channel.id_start]
            if isinstance(component, SolarController):
                channel = self._update_solar_channel_model_data(component, channel)

    def _update_solar_panel_model_data(self, component: Component, component_gui: ComponentGui) -> ComponentGui:
        """Updates solar panel gui data model."""
        component_gui.model.thumbnail_chart_data1 = component.power_history
        component_gui.model.main_icon_data = f"{component.rated_power_kWh:.2f} kWh\n  {component.efficiency:.1f}%"
        component_gui.model.thumbnail_chart_timestamp = component.power_history_timestamps
        component_gui.update_component()
        return component_gui

    def _update_solar_channel_model_data(self, component: Component, channel_gui: Channel) -> Channel:
        """Updates solar panel channel gui data model."""
        channel_gui.model.text = f"{component.power_kWh} kWh"
        channel_gui.model.arrow_color = QColor(0, 0, 255, 200) if component.power_kWh >= 0 else QColor(255, 0, 0, 200)
        channel_gui.model.arrow_density = component.efficiency / 2
        channel_gui.model.arrows_reversed = False if component.power_kWh >= 0 else True
        channel_gui.update_channel()
        return channel_gui

    def _update_battery_model_data(self, component: Component, component_gui: ComponentGui) -> ComponentGui:
        """Updates battery gui data model."""
        component_gui.model.main_icon_data = f"{component.battery_capacity_kWh:.2f} kWh\n  {component.charge_percent:.1f}%"
        component_gui.model.thumbnail_chart_data1 = component.charge_history
        component_gui.model.thumbnail_chart_timestamp = component.charge_history_timestamps
        component_gui.update_component()
        return component_gui
