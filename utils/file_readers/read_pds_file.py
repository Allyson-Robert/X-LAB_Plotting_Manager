import csv


def read_pds_file(path: str) -> list:
    skip_lines = 10
    nr_cols = 11

    # Retrieve the delimiter by sniffing the file
    with open(path) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        # Skip lines
        header = ""
        for i in range(skip_lines):
            header += str(next(reader))
            header += "\n"

        # Prepare data matrix with 12 lists
        data = [header]
        for col in range(nr_cols):
            data.append([])

        # Fill the rows of the data matrix line by line
        for line in reader:
            for col in range(1, nr_cols + 1):
                data[col].append(line[col - 1])

    return data
