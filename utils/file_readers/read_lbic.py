import csv
import numpy as np


def read_lbic(path: str) -> list:
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        # First row is x-axis positions (ignore very first element)
        x = [float(intensity.replace(',', '.')) for intensity in next(reader)][1:]

        y = []
        z = []
        for line in reader:
            # First element of each row is y-axis position
            y.append(float(line[0].replace(',', '.')))

            # Data contained in the rest of the row
            row = [float(intensity.replace(',', '.')) for intensity in line[1:]]

            # TODO: Check why this was necessary
            if np.count_nonzero(row):
                z.append(row)
    return [x, y, z]
