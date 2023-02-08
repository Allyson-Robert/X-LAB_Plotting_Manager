from data.data_processors.data_processors import ScatterDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVScatterData
import utils.calc.iv_calc as iv_calc
import numpy as np


class IVScatterDataProcessor(ScatterDataProcessor):
    def __init__(self, iv_data: IVScatterData):
        self.data = iv_data

        self._processing_functions = {
            "power": self.calculate_power,
            "forward_voltage": self.get_forward_voltage,
            "forward_current": self.get_forward_current,
            "forward_power": self.get_forward_power,
            "reverse_voltage": self.get_reverse_voltage,
            "reverse_current": self.get_reverse_current,
            "reverse_power": self.get_reverse_power,
            "truncated_voltage": self.get_truncated_voltage,
            "truncated_current": self.get_truncated_current,
            "truncated_power": self.get_truncated_power,
            "current_difference": self.get_current_difference,
            "power_difference": self.get_power_difference,
            "isc": self.find_isc,
            "voc": self.find_voc,
            "mpp_power": self.calculate_mpp_power,
            "mpp_voltage": self.calculate_mpp_voltage,
            "mpp_current": self.calculate_mpp_current,
            "mpp_resistance": self.calculate_mpp_resistance,
            "fill_factor": self.calculate_fill_factor,
            "series_resistance": self.calculate_series_resistance,
            "shunt_resistance": self.calculate_shunt_resistance
        }
        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    def get_data(self, observable: str):
        # Return raw data
        if observable in self.data.get_allowed_observables():
            return self.data.get_data(observable)

        # Compute processed data if needed
        elif observable in self._processed_observables:
            if self.processed_data[observable] is None:
                self.processed_data[observable] = self._processing_functions[observable]()
            return self.processed_data[observable]
        else:
            raise ValueError(f"IVScatterData does not contain {observable} data")

    def calculate_power(self):
        current = self.data.get_data("current")
        voltage = self.data.get_data("voltage")
        power = []
        for i, v in zip(current, voltage):
            power.append(abs(i * v))

        return power

    def get_forward_voltage(self) -> list:
        voltage = self.data.get_data("voltage")
        return iv_calc.get_forward(voltage)

    def get_forward_current(self) -> list:
        current = self.data.get_data("current")
        return iv_calc.get_forward(current)

    def get_forward_power(self) -> list:
        power = self.get_data("power")
        return iv_calc.get_forward(power)

    def get_reverse_voltage(self) -> list:
        voltage = self.data.get_data("voltage")
        return iv_calc.get_reverse(voltage)

    def get_reverse_current(self) -> list:
        current = self.data.get_data("current")
        return iv_calc.get_reverse(current)

    def get_reverse_power(self) -> list:
        power = self.get_data("power")
        return iv_calc.get_reverse(power)

    def get_truncated_voltage(self) -> list:
        voc = self.get_data("voc")
        return iv_calc.truncate_list(self.get_data("voltage"), 0, voc)

    def get_truncated_current(self) -> list:
        # TODO: Check signs, this might not work as intended
        isc = self.get_data("isc")
        return iv_calc.truncate_list(self.get_data("current"), -isc, 0)

    def get_truncated_power(self) -> list:
        return []

    def get_current_difference(self) -> list:
        return []

    def get_power_difference(self) -> list:
        return []

    def find_isc(self) -> float:
        """
        The short-circuit current is the current at zero voltage. This is the y-crossing in an IV curve
        """
        current = self.data.get_data("current")
        voltage = self.data.get_data("voltage")
        return abs(iv_calc.find_crossing(voltage, current))

    def find_voc(self) -> float:
        """
        The open-circuit voltage is the voltage where there is no current. This is the x-crossing in an IV curve.
        Equivalently one can find the y-crossing in a VI curve,
        """
        current = self.data.get_data("current")
        voltage = self.data.get_data("voltage")
        return abs(iv_calc.find_crossing(current, voltage))

    def calculate_mpp_power(self) -> float:
        return 0.0

    def calculate_mpp_voltage(self) -> float:
        return 0.0

    def calculate_mpp_current(self) -> float:
        return 0.0

    def calculate_mpp_resistance(self) -> float:
        return 0.0

    def truncate_forward_iv(self):
        pass

    def find_mpp(self) -> dict:
        pass

    def calculate_fill_factor(self) -> float:
        pass

    def calculate_series_resistance(self) -> dict:
        pass

    def calculate_series_resistance(self) -> dict:
        pass
