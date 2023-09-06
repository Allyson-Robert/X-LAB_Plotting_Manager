import plotly.colors


def get_colour(colorscale, value):
    """
    Plotly continuous colorscales assign colors to the range [0, 1]. This function computes the intermediate color for any value in that range.
    """
    if len(colorscale) < 1:
        raise ValueError("colorscale must have at least one color")

    if value <= 0 or len(colorscale) == 1:
        return colorscale[0][1]
    if value >= 1:
        return colorscale[-1][1]

    for cutoff, color in colorscale:
        if value > cutoff:
            low_cutoff, low_color = cutoff, color
        else:
            high_cutoff, high_color = cutoff, color
            break

    # noinspection PyUnboundLocalVariable
    return plotly.colors.find_intermediate_color(
        lowcolor=low_color, highcolor=high_color,
        intermed=((value - low_cutoff) / (high_cutoff - low_cutoff)),
        colortype="rgb")