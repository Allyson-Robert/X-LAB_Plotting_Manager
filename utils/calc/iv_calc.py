import numpy as np


def is_illuminated(input_currents: list) -> bool:
    # Check the first quarter of the list
    sample = input_currents[:int(len(input_currents) / 4)]
    average_current = np.average(sample)
    # TODO: Check this cutoff, not sure that -0.1 uA is sufficiently low
    # return average_current < -10**(-7)
    return True


def get_forward(input: list) -> list:
    half_len = int(len(input)/2)
    return input[:half_len]


def get_reverse(input: list) -> list:
    half_len = int(len(input)/2)
    return input[half_len:]


def contiguous_trimmed_sublist(input: list, lower: float, upper: float) -> list:
    """
        Will return a list that starts right before the 'lower' value and ends right after the 'upper' value.
        List must increase/decrease monotonically
    """
    output = []
    # Catch lower edge
    if lower < input[1]:
        output.append(input[0])

    # Walk through input from 'second' to 'second-to-last' elements
    for index in range(1, len(input) - 1):
        if lower < input[index + 1] and input[index - 1] < upper:
            output.append(input[index])

    # Catch upper edge
    if upper > input[-2]:
        output.append(input[-1])
    return output


def contiguous_sub_list(input: list, threshold: float, above: bool) -> list:
    """
        Get all values of a list above or below a certain threshold. Powered by ChatGPT
    """
    start = None
    end = None

    for i, num in enumerate(input):
        # If above is True then num must be above threshold, if not it must be below
        if (above and num >= threshold) or (not above and num <= threshold):
            # Mark the start if the sub_list as soon as the threshold is reached
            if start is None:
                start = i
        # Once threshold has been reached and we dip back below (or rise above) the threshold, mark the end
        elif start is not None and end is None:
            end = i

    # If a start has been found return sublist
    if start is not None:
        end = len(input)
        return input[start:end]

    # If no start was found, raise error
    raise ValueError(f"Input list has no elements crossing the threshold: {threshold}")


def find_crossing(x: list, y:list) -> float:
    """
        Determine interpolated y-crossing for a given numerical plot.
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