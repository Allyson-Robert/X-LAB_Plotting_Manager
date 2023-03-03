def export_to_csv(filename: str, list_of_lists: list, delimiter: str = '\t'):
    first_list = list_of_lists[0]

    with open(filename, 'w') as csv_file:
        for index in range(len(first_list)):
            row = []
            for sublist in list_of_lists:
                row.append(str(sublist[index]))
            csv_file.write(delimiter.join(row))
            csv_file.write('\n')
