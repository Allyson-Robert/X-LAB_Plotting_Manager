import plotly.graph_objects as go


def find_figure_range(fig, axis='x'):
    lower = []
    upper = []
    for datum in fig.data:
        lower.append(datum[axis][0])
        upper.append(datum[axis][-1])

    return [min(lower), max(upper)]