def flatten_matrix(input: list[list]) -> list:
    output = []
    for sublist in input:
        for item in sublist:
            output.append(item)
    return output