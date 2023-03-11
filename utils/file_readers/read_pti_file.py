import csv
from utils.file_readers.read_csv import read_csv


def read_pti_file(filename):
    # Two options for the contents of the file, will open both
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        line = next(reader)
        print(line)
        # If two columns: straight up data
        if len(line) == 2:
            return read_csv(filename, delimiter = '\t')

        # If four columns: additional metadata in the first column
        elif len(line) == 4:
            data = [[], []]
            with open(filename) as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                # Ignore the second column
                for [x, y, z, w] in reader:
                    if 'D1' not in x:
                        continue
                    if z and w:
                        z = float(z.replace(',', '.'))
                        w = float(w.replace(',', '.'))
                        if z > 0 and w > 0:
                            data[0].append(z)
                            data[1].append(w)
            return data
        else:
            return None
