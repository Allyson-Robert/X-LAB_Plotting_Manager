import plotly.graph_objects as go
from utils.plot_preppers.find_figure_range import find_figure_range
import numpy as np


# Function to create and display a colorbar for a custom color scale
#FIXME: Scale adds dummy trace that is visible, also has a title
def show_colourscale(colorscale, fig, title="Elapsed Time"):
    # Add an invisible heatmap to show the colorbar based on the custom colorscale
    trace_range = find_figure_range(fig, axis='customdata')

    fig.add_trace(go.Heatmap(
        z=[trace_range],  # Minimal data just to trigger the colorbar
        colorscale=colorscale,
        showscale=True,
        colorbar=dict(
            orientation='h',   # Horizontal colorbar
            x=0.5,             # Center the colorbar
            xanchor='center',
            thickness=20,      # Thickness of the colorbar
            len=1.0,           # Make the colorbar as wide as the figure
            y=-0.3,            # Position the colorbar below the figure
            yanchor='top'
        ),
        hoverinfo='none',  # Remove hover info from the dummy heatmap
        opacity=0  # Make the heatmap fully transparent
    ))

    return fig