import numpy as np


def get_forward(input: list) -> list:
    half_len = len(input)/2
    return input[:half_len + 1]


def get_reverse(input: list) -> list:
    half_len = len(input)/2
    return input[half_len + 1:]


def truncate_list(input: list, lower: float, upper: float) -> list:
    """
        Will return a list that starts right before the 'lower' value and ends right after the 'upper' value
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

def find_crossing(x: list, y:list) -> float:
    """
        Determine interpolated y-crossing for a given numerical plot.
    """
    # To find the y-crossing we seek the point where the current turns positive
    index_before = 0
    index_after = len(y)
    for index in range(len(y)):
        if y[index + 1] > 0:
            index_before = index
            index_after = index + 1
            break

    # Once the numerical y-crossing has been found: determine the interpolated y-crossing (V = 0)
    crossing = np.interp(0, x[index_before:index_after], y[index_before:index_after])
    return crossing