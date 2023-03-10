from data.data_processors.data_processors import DataProcessorCore
from data.datatypes.scatter_data.iv_scatter import IVData
import utils.calc.iv_calc as iv_calc
from utils.errors.errors import VocNotFoundError, IscNotFoundError, ObservableNotComputableError


class IVScatterDataProcessor(DataProcessorCore):
    def __init__(self, iv_data: IVData):
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

    # # TODO: Is this really necessary?  Ignores Datatype observables
    # def get_allowed_observables(self):
    #     return self._processed_observables

    def validate_observables(self, *args):
        # Checks whether all desired observables can be obtained for this data
        try:
            for observable in args:
                self.get_data(observable)
        except VocNotFoundError:
            raise ObservableNotComputableError

    # TODO: Deprecate?
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
        isc = self.get_data("isc")
        voc = self.get_data("voc")
        voltage = self.get_data("forward_voltage")
        current = self.get_data("forward_current")

        trimmed_voltage = iv_calc.trim_iv(voltage, current, voltage, isc, voc)
        return {"units": "Voltage (V)", "data": trimmed_voltage}

    def get_truncated_current(self) -> dict:
        isc = self.get_data("isc")
        voc = self.get_data("voc")
        voltage = self.get_data("forward_voltage")
        current = self.get_data("forward_current")

        trimmed_current = iv_calc.trim_iv(voltage, current, current, isc, voc)
        return {"units": "Current (A)", "data": trimmed_current}

    def get_truncated_power(self) -> dict:
        isc = self.get_data("isc")
        voc = self.get_data("voc")
        voltage = self.get_data("forward_voltage")
        current = self.get_data("forward_current")
        power = self.get_data("forward_power")
        try:
            trimmed_power = iv_calc.trim_iv(voltage, current, power, isc, voc)
        except IndexError:
            raise ObservableNotComputableError("Error in power truncation, issue probably related to dark measurement")

        return {"units": "Power (W)", "data": trimmed_power}

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
            isc = iv_calc.find_crossing(voltage, current)
            # TODO: Is there any physical check that can be placed on Isc?
            return {"units": "Current (A)", "data": abs(isc)}
        except IndexError as ie:
            raise IscNotFoundError

    def find_voc(self) -> dict:
        """
        The open-circuit voltage is the voltage where there is no current. This is the x-crossing in an IV curve.
        Equivalently one can find the y-crossing in a VI curve,
        """
        current = self.get_data("forward_current")
        voltage = self.get_data("forward_voltage")
        try:
            voc = iv_calc.find_crossing(current, voltage)
            if voc < 0:
                raise VocNotFoundError("Voc was found to be negative")
            return {"units": "Voltage (V)", "data": voc}
        except IndexError as ie:
            raise VocNotFoundError("Voc could not be determined from the data")

    def calculate_mpp_power(self) -> dict:
        power = self.get_data("truncated_power")
        if len(power) < 1:
            raise ObservableNotComputableError("Truncated power is empty")
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
        try:
            ff = max_power/(voc * isc)
        except ZeroDivisionError:
            raise ObservableNotComputableError("Voc or Isc are too small throwing a div by zero error")
        return {"units": "Fill ~factor", "data": ff}

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
