def export_to_csv(filename: str, list_of_lists: list, header: list, delimiter: str = '\t'):
    """
    Export matrix to a delimiter-separated text file.

    Parameters
    ----------
    filename:
        Path to the output file that will be created/overwritten.
    list_of_lists:
        List of equal-length iterables, each representing a column of data.
    header:
        List of column labels written as the first line of the file.
    delimiter:
        String used to join header fields and row values (defaults to tab).

    Notes
    -----
    The function assumes that all columns in ``list_of_lists`` have the same
    length and will raise ``IndexError`` if this is not the case.
    """
    first_list = list_of_lists[0]

    # Open a file
    with open(filename, 'w') as csv_file:
        # Save the header row
        csv_file.write(delimiter.join(header))
        csv_file.write('\n')

        # Go through all columns and write the data
        for index in range(len(first_list)):
            row = []
            for sublist in list_of_lists:
                row.append(str(sublist[index]))
            csv_file.write(delimiter.join(row))
            csv_file.write('\n')
