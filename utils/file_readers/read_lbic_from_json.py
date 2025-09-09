import json


def read_lbic_from_json(path: str) -> list:
    with open(path, 'r') as f:
        data = json.load(f)

    try:
        # This is the naming convention for the newest version of the LBIC fw
        x_steps = data["x pixels"]
        y_steps = data["y pixels"]
        step_size = data["pixel size"]
        z = data["photocurrent scan"]
    except KeyError:
        # Keeping this for bw compatibility, old version assumed pixels to be of equal size to steps
        x_steps = data["x steps"]
        y_steps = data["y steps"]
        step_size = data["step size"]
        z = data["photocurrent scan"]

    # Create x and y axis arrays based on step size and number of steps
    x = [i * step_size for i in range(x_steps)]  # mm
    y = [i * step_size for i in range(y_steps)]  # mm

    return [x, y, z]