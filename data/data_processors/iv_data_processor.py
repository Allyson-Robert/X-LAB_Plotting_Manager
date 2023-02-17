from data.data_processors.data_processors import ScatterDataProcessor
from data.datatypes.scatter_data.iv_scatter import IVScatterData
import utils.calc.iv_calc as iv_calc
from utils.errors import VocNotFound, IscNotFound


class IVScatterDataProcessor(ScatterDataProcessor):
    def __init__(self, iv_data: IVScatterData):
        self.data = iv_data

        self._processing_functions = {
            "is_illuminated": {
                "function": self.is_illuminated,
                "is_illuminated": False
            },
            "power": {
                "function": self.calculate_power,
                "is_illuminated": False
            },
            "forward_voltage": {
                "function": self.get_forward_voltage,
                "is_illuminated": False
            },
            "forward_current": {
                "function": self.get_forward_current,
                "is_illuminated": False
            },
            "forward_power": {
                "function": self.get_forward_power,
                "is_illuminated": False
            },
            "reverse_voltage": {
                "function": self.get_reverse_voltage,
                "is_illuminated": False
            },
            "reverse_current": {
                "function": self.get_reverse_current,
                "is_illuminated": False
            },
            "reverse_power": {
                "function": self.get_reverse_power,
                "is_illuminated": False
            },
            "truncated_voltage": {
                "function": self.get_truncated_voltage,
                "is_illuminated": True
            },
            "truncated_current": {
                "function": self.get_truncated_current,
                "is_illuminated": True
            },
            "truncated_power": {
                "function": self.get_truncated_power,
                "is_illuminated": False
            },
            "current_difference": {
                "function": self.get_current_difference,
                "is_illuminated": False
            },
            "power_difference": {
                "function": self.get_power_difference,
                "is_illuminated": False
            },
            "isc": {
                "function": self.find_isc,
                "is_illuminated": True
            },
            "voc": {
                "function": self.find_voc,
                "is_illuminated": True
            },
            "mpp_power": {
                "function": self.calculate_mpp_power,
                "is_illuminated": True
            },
            "mpp_voltage": {
                "function": self.calculate_mpp_voltage,
                "is_illuminated": True
            },
            "mpp_current": {
                "function": self.calculate_mpp_current,
                "is_illuminated": True
            },
            "mpp_resistance": {
                "function": self.calculate_mpp_resistance,
                "is_illuminated": True
            },
            "fill_factor": {
                "function": self.calculate_fill_factor,
                "is_illuminated": True
            },
            "series_resistance": {
                "function": self.calculate_series_resistance,
                "is_illuminated": True
            },
            "shunt_resistance": {
                "function": self.calculate_shunt_resistance,
                "is_illuminated": True
            },
            "parameters": {
                "function": self.get_parameters,
                "is_illuminated": True
            }
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
                self.processed_data[observable] = self._processing_functions[observable]["function"]()
            return self.processed_data[observable]['data']
        else:
            raise ValueError(f"IVScatterData does not contain {observable} data")

    def get_units(self, observable: str) -> str:
        self.get_data(observable)
        # Return raw data
        if observable in self.data.get_allowed_observables():
            return self.data.get_units(observable)
        elif observable in self._processed_observables:
            return self.processed_data[observable]["units"]
        else:
            raise ValueError(f"IVScatterData does not contain {observable} data")

    def is_illuminated(self):
        current = self.get_data("forward_current")
        return {"units": None, "data": iv_calc.is_illuminated(current)}

    def calculate_power(self):
        current = self.data.get_data("current")
        voltage = self.data.get_data("voltage")
        power = []
        for i, v in zip(current, voltage):
            power.append(abs(i * v))

        return {"units": "Power (W)", "data": power}

    def get_forward_voltage(self) -> dict:
        voltage = self.data.get_data("voltage")
        return {"units": "Voltage (V)", "data": iv_calc.get_forward(voltage)}

    def get_forward_current(self) -> dict:
        current = self.data.get_data("current")
        return {"units": "Current (A)", "data": iv_calc.get_forward(current)}

    def get_forward_power(self) -> dict:
        power = self.get_data("power")
        return {"units": "Power (W)", "data": iv_calc.get_forward(power)}

    def get_reverse_voltage(self) -> dict:
        voltage = self.data.get_data("voltage")
        return {"units": "Voltage (V)", "data": iv_calc.get_reverse(voltage)}

    def get_reverse_current(self) -> dict:
        current = self.data.get_data("current")
        return {"units": "Current (A)", "data": iv_calc.get_reverse(current)}

    def get_reverse_power(self) -> dict:
        power = self.get_data("power")
        return {"units": "Power (W)", "data": iv_calc.get_reverse(power)}

    # TODO: These truncations are not guaranteed to be aligned. All of these should truncate between Isc and Voc
    def get_truncated_voltage(self) -> dict:
        voc = self.get_data("voc")
        voltage = self.get_data("forward_voltage")
        return {"units": "Voltage (V)", "data": iv_calc.contiguous_trimmed_sublist(voltage, 0, voc)}

    def get_truncated_current(self) -> dict:
        isc = self.get_data("isc")
        current = self.get_data("forward_current")
        return {"units": "Current (A)", "data": iv_calc.contiguous_trimmed_sublist(current, -isc, 0)}

    def get_truncated_power(self) -> dict:
        power = self.get_data("forward_power")
        return {"units": "Power (W)", "data": iv_calc.contiguous_sub_list(power, threshold=0, above=True)}

    def get_current_difference(self) -> dict:
        fw_current = self.get_data("forward_current")
        rv_current = self.get_data("reverse_current")
        return {"units": "Current (A)", "data": [i - j for i, j in zip(fw_current, rv_current[::-1])]}

    def get_power_difference(self) -> dict:
        fw_power = self.get_data("forward_power")
        rv_power = self.get_data("reverse_power")
        return {"units": "Power (W)", "data": [p - q for p, q in zip(fw_power, rv_power[::-1])]}

    def find_isc(self) -> dict:
        """
        The short-circuit current is the current at zero voltage. This is the y-crossing in an IV curve
        """
        current = self.get_data("forward_current")
        voltage = self.get_data("forward_voltage")
        try:
            return {"units": "Current (A)", "data": abs(iv_calc.find_crossing(voltage, current))}
        except IndexError as ie:
            raise IscNotFound

    def find_voc(self) -> dict:
        """
        The open-circuit voltage is the voltage where there is no current. This is the x-crossing in an IV curve.
        Equivalently one can find the y-crossing in a VI curve,
        """
        current = self.get_data("forward_current")
        voltage = self.get_data("forward_voltage")
        try:
            return {"units": "Voltage (V)", "data": iv_calc.find_crossing(current, voltage)}
        except IndexError as ie:
            raise VocNotFound

    def calculate_mpp_power(self) -> dict:
        power = self.get_data("truncated_power")
        return {"units": "Power (W)", "data": max(power)}

    def calculate_mpp_voltage(self) -> dict:
        max_power = self.get_data("mpp_power")
        power = self.get_data("power")
        voltage = self.get_data("voltage")

        return {"units": "Voltage (V)", "data": voltage[power.index(max_power)]}

    def calculate_mpp_current(self) -> dict:
        max_power = self.get_data("mpp_power")
        power = self.get_data("power")
        current = self.get_data("current")

        return {"units": "Current (A)", "data": abs(current[power.index(max_power)])}

    def calculate_mpp_resistance(self) -> dict:
        mpp_current = self.get_data("mpp_current")
        mpp_voltage = self.get_data("mpp_voltage")
        return {"units": "Resistance (\Omega)", "data": mpp_voltage/mpp_current}

    def calculate_fill_factor(self) -> dict:
        voc = self.get_data("voc")
        isc = self.get_data("isc")
        max_power = self.get_data("mpp_power")
        return {"units": "Fill factor", "data": max_power/(voc * isc)}

    def calculate_series_resistance(self) -> dict:
        current = self.get_data("current")
        voltage = self.get_data("voltage")
        return {"units": "Resistance (\Omega)", "data": iv_calc.find_local_slope(voltage, current, 0)}

    def calculate_shunt_resistance(self) -> dict:
        current = self.get_data("current")
        voltage = self.get_data("voltage")
        return {"units": "Resistance (\Omega)", "data": 1/iv_calc.find_local_slope(current, voltage, 0)}

    def get_parameters(self) -> dict:
        return {"units": "N/A", "data": {
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
        }
