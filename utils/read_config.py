import json

def read_config(config_path: str) -> dict:
    """Read a JSON configuration file and return its contents as a dictionary.

    Parameters
    ----------
    config_path : str
        The file path to the JSON configuration file.

    Returns
    -------
    dict
        A dictionary containing the configuration settings.
    """
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config