import numpy as np


# CHECK: Deprecate?
def is_illuminated(input_currents: list) -> bool:
    # Checks the first quarter of the list
    sample = input_currents[:int(len(input_currents) / 4)]
    average_current = np.average(sample)
    # FIXME: Check this cutoff, not sure that -0.1 uA is sufficiently low
    # return average_current < -10**(-7)
    return True


def get_forward(input: list) -> list:
    half_len = int(len(input)/2)
    return input[:half_len]


def get_reverse(input: list) -> list:
    half_len = int(len(input)/2)
    return input[half_len:]


def split_forward_reverse(independent: list, dependent: list) -> tuple[list, list, list, list]:
    """
    Assuming a behaviour for the independent list in two parts, a monotonic increase followed by a monotonic decrease.
    Under this assumption the function will split both independent and dependent lists by finding when the first
    reverses.

    :param independent:
    :param dependent:
    :return:

    """

    # Find the index at which the list reverses direction
    change = np.diff(independent)
    direction = [np.sign(v) for v in change]
    reversing_index = direction.index(-1)

    return independent[:reversing_index], independent[reversing_index:], dependent[:reversing_index], dependent[reversing_index:]


def trim_iv(voltages: list, currents: list, to_trim: list, isc: float, voc: float) -> list:
    """
        Will return a list that is trimmed based on the IV curve, Voc and Isc.

        This function assumes a monotonic increase of voltage (independent var -> ok) and current (noise -> not sure).
        The last current value below Isc and the first voltage value above Voc are searched, their indexes found and
        a the to_trim list is sublisted between the two indices.
    """
    # Find the index of the last negative voltage, this will have been the one used for Isc
    low = voltages.index([v for v in voltages if v < 0][-1])
    # Find all voltage values above voc and return the index of the first
    high = voltages.index([v for v in voltages if v > voc][0]) + 1

    # Return all powers inbetween, note slicing goes up to but not including 'high'
    return to_trim[low:high]


def find_crossing(x: list, y:list) -> float:
    """
        Determine interpolated y-crossing for a given numerical plot. Could be confused by excessively noisy x-data.
    """
    # To find the y-crossing we seek the point where the x-data turns positive
    for index in range(len(x)):
        if x[index + 1] > 0:
            break
    # Once the numerical y-crossing has been found: determine the interpolated y-crossing (x = 0)
    crossing = np.interp(0, x[index:index+2], y[index:index+2])
    return crossing


def find_local_slope(x: list, y: list, value: float) -> float:
    for i, v in enumerate(y):
        if y[i] < value < y[i + 1]:
            break
    return (y[i] - y[i+1])/(x[i] - x[i+1])