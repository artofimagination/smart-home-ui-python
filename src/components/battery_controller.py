import random

from components.component import Component


class BatteryController(Component):
    """This controller handles all chemical battery related data and management control."""
    def __init__(self):
        super(BatteryController, self).__init__()
        self.battery_charge_kWh = 0
        self.battery_capacity_kWh = 36
        self.charge_percent = 0
        self.charge_history = list()
        self.charge_history_timestamps = list()
        self.timestamp = 0

    def generate_demo_data(self):
        """Generates a demo/functional test data."""
        self.battery_charge_kWh += random.randint(10, 40) / 1000
        self.charge_percent = self.battery_charge_kWh * 100.0 / self.battery_capacity_kWh
        self.charge_history.append(self.battery_charge_kWh)
        self.timestamp += 1
        self.charge_history_timestamps.append(self.timestamp)
        if len(self.charge_history) > 50:
            self.charge_history.pop(0)
            self.charge_history_timestamps.pop(0)
