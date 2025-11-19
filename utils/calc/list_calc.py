def flatten_matrix(input: list[list]) -> list:
    if len(input) < 1:
        raise ValueError("Flatten Matrix Will not Flatten empty list")
    output = []
    for sublist in input:
        for item in sublist:
            output.append(item)
    return output
