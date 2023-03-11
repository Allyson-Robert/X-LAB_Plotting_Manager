import plotly.graph_objects as go


def heatmap_prepper(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        yaxis_scaleanchor="x",
        width=660,
        height=600,
        font=dict(
            family="Open Sans",
            size=18,
            color="RebeccaPurple"
        ),
    )

    # Style bg
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_xaxes(visible=False)
    fig['layout']['yaxis']['autorange'] = "reversed"

    return fig


def add_profiles(fig: go.Figure) -> go.Figure:
    fig.update_yaxes(
        showspikes=True,
        spikemode="across",
        spikethickness=0.5
    )
    fig.update_xaxes(
        showspikes=True,
        spikemode="across",
        spikethickness=0.5
    )
    return fig