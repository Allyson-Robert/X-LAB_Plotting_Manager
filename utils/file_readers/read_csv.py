import csv


def read_csv(path):
    # Retrieve the delimiter by sniffing the file
    with open(path) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read())
        sep = dialect.delimiter

    # Actually start reading the file
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter=sep)
        data = [[], []]
        for [x, y] in reader:
            if x and y:
                data[0].append(float(x.replace(',', '.')))
                data[1].append(float(y.replace(',', '.')))
    return data
