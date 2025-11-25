import re


def split_camel_case(camel_case) -> list[str]:
    """
    Split a CamelCase string into its component words.

    Examples
    --------
    "MyPlotType" → ["My", "Plot", "Type"]

    Parameters
    ----------
    camel_case : str
        Input CamelCase string.

    Returns
    -------
    list[str]
        List of lowercase/uppercase-correct word segments.
    """
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', camel_case)