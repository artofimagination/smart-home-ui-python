from components.component import Component


class BatteryController(Component):
    """This controller handles all chemical battery related data and management control."""
    def __init__(self):
        self.battery_charge_kWh = 0
