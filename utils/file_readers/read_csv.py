import csv


def read_csv(path, skip_lines=0, delimiter=None) -> list:
    # Retrieve the delimiter by sniffing the file
    if delimiter is None:
        with open(path) as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read())
            delimiter = dialect.delimiter

    # Actually start reading the file
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)

        # Skip lines
        for i in range(skip_lines):
            next(reader)

        data = [[], []]
        # print(delimiter, next(reader))
        for line in reader:
            # print(line)
            x = line[0]
            y = line[1]

            if x and y:
                data[0].append(float(x.replace(',', '.')))
                data[1].append(float(y.replace(',', '.')))
    return data
