def read_aalto_iv_csv(file_path):
    # Read file and split into blocks by empty lines
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    blocks = [
        [line.strip() for line in b.split("\n") if line.strip()]
        for b in content.split("\n\n")
        if b.strip()
    ]

    # There must be four blocks exactly, if different from 4 check if multiple
    if len(blocks) != 4:
        if len(blocks) % 4 == 0:
            # In the future this should be dynamically split before instructing the user to restart
            raise ValueError("File contains more than one measurement, copy desired measurement in a separate file.")
        raise ValueError("Unexpected file format: expected (multiples of) four blocks, separated by a blank line.")

    for index in range(4):
        if len(blocks[0]) != 3:
            raise ValueError("Metadata block must have at least 3 lines")
    return blocks
