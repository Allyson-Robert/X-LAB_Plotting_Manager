import plotly.graph_objects as go


def scatter_prepper(fig: go.Figure) -> go.Figure:
    # Format title
    fig.update_layout(
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
    )

    # Format font
    fig.update_layout(
        font=dict(
            family="Open Sans",
            size=18,
            color="RebeccaPurple"
        ),
    )

    # Format background colours
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Format axes
    fig.update_xaxes(
        showline=True,
        linewidth=2,
        linecolor='black',
        ticks="outside"
    )

    fig.update_yaxes(
        showline=True,
        linewidth=2,
        linecolor='black',
        ticks="outside"
    )

    # No Grid
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig
