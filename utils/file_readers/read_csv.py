import csv


def read_csv(path, skip_lines=0) -> list:
    # Retrieve the delimiter by sniffing the file
    with open(path) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read())
        sep = dialect.delimiter

    # Actually start reading the file
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=sep)

        # Skip lines
        for i in range(skip_lines):
            next(reader)

        data = [[], []]
        for [x, y] in reader:
            if x and y:
                data[0].append(float(x.replace(',', '.')))
                data[1].append(float(y.replace(',', '.')))
    return data
