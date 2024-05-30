import random

from components.component import Component


class SolarController(Component):
    """
        This controller is responsible to manage solar panel data and to control the panels.
        All charts panel and panal array related actions and data lives here.
    """
    def __init__(self):
        super(SolarController, self).__init__()
        random.seed(1000)
        self.voltage_V = 0
        self.rated_power_kWh = 10
        self.power_kWh = 0
        self.power_history = list()
        self.power_history_timestamps = list()
        self.efficiency = 0
        self.timestamp = 0

    def generate_demo_data(self):
        """Generates a demo/functional test data."""
        self.power_kWh = random.randint(800, 1000) / 100
        self.voltage_V = random.randint(0, 24000) / 1000
        self.efficiency = self.power_kWh * 100.0 / self.rated_power_kWh
        self.power_history.append(self.power_kWh)
        self.timestamp += 1
        self.power_history_timestamps.append(self.timestamp)
        if len(self.power_history) > 50:
            self.power_history.pop(0)
            self.power_history_timestamps.pop(0)
