from data.data_processors.data_processors import ScatterDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVScatterData
import utils.calc.iv_calc as iv_calc


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
            "shunt_resistance": self.calculate_shunt_resistance,
            "parameters": self.get_parameters
        }
        self.processed_data = {}
        for key in self._processing_functions:
            self.processed_data[key] = None

        self._processed_observables = self.processed_data.keys()

    def get_allowed_observables(self):
        return self._processed_observables

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
        voltage = self.get_data("forward_voltage")
        return iv_calc.contiguous_trimmed_sublist(voltage, 0, voc)

    def get_truncated_current(self) -> list:
        # TODO: Check signs, this might not work as intended
        isc = self.get_data("isc")
        current = self.get_data("forward_current")
        return iv_calc.contiguous_trimmed_sublist(current, -isc, 0)

    def get_truncated_power(self) -> list:
        power = self.get_data("forward_power")
        return iv_calc.contiguous_sub_list(power, threshold=0, above=True)

    def get_current_difference(self) -> list:
        fw_current = self.get_data("forward_current")
        rv_current = self.get_data("reverse_current")
        return [i - j for i, j in zip(fw_current, rv_current[::-1])]

    def get_power_difference(self) -> list:
        fw_power = self.get_data("forward_power")
        rv_power = self.get_data("reverse_power")
        return [p - q for p, q in zip(fw_power, rv_power[::-1])]

    def find_isc(self) -> float:
        """
        The short-circuit current is the current at zero voltage. This is the y-crossing in an IV curve
        """
        current = self.get_data("forward_current")
        voltage = self.get_data("forward_voltage")
        return abs(iv_calc.find_crossing(voltage, current))

    def find_voc(self) -> float:
        """
        The open-circuit voltage is the voltage where there is no current. This is the x-crossing in an IV curve.
        Equivalently one can find the y-crossing in a VI curve,
        """
        current = self.get_data("forward_current")
        voltage = self.get_data("forward_voltage")
        return abs(iv_calc.find_crossing(current, voltage))

    def calculate_mpp_power(self) -> float:
        power = self.get_data("truncated_power")
        return max(power)

    def calculate_mpp_voltage(self) -> float:
        max_power = self.get_data("mpp_power")
        power = self.get_data("power")
        voltage = self.get_data("voltage")

        return voltage[power.index(max_power)]

    def calculate_mpp_current(self) -> float:
        max_power = self.get_data("mpp_power")
        power = self.get_data("power")
        current = self.get_data("current")

        return abs(current[power.index(max_power)])

    def calculate_mpp_resistance(self) -> float:
        mpp_current = self.get_data("mpp_current")
        mpp_voltage = self.get_data("mpp_voltage")
        return mpp_voltage/mpp_current

    def calculate_fill_factor(self) -> float:
        voc = self.get_data("voc")
        isc = self.get_data("isc")
        max_power = self.get_data("mpp_power")
        return max_power/(voc * isc)

    def calculate_series_resistance(self) -> float:
        current = self.get_data("current")
        voltage = self.get_data("voltage")
        return iv_calc.find_local_slope(voltage, current, 0)

    def calculate_shunt_resistance(self) -> float:
        current = self.get_data("current")
        voltage = self.get_data("voltage")
        return 1/iv_calc.find_local_slope(current, voltage, 0)

    def get_parameters(self) -> dict:
        return {
            "label": self.get_data("label"),
            "isc": self.get_data("isc"),
            "voc": self.get_data("voc"),
            "fill_factor": self.get_data("fill_factor"),
            "mpp_power": self.get_data("mpp_power"),
            "mpp_voltage": self.get_data("mpp_voltage"),
            "mpp_current": self.get_data("mpp_current"),
            "mpp_resistance": self.get_data("mpp_resistance"),
            "rsh": self.get_data("shunt_resistance"),
            "rs": self.get_data("series_resistance")
        }
