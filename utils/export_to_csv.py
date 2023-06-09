def export_to_csv(filename: str, list_of_lists: list, header: list, delimiter: str = '\t'):
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
