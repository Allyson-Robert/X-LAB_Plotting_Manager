from plotly.subplots import make_subplots
import plotly.graph_objects as go


def four_subplots_prepper() -> go.Figure:
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("A", "B", "C", "D")
    )

    # edit axis labels
    fig['layout']['xaxis']['title'] = '$Time ~(hrs)$'
    fig['layout']['yaxis']['title'] = '$I_{sc} ~(A)$'

    fig['layout']['xaxis2']['title'] = '$Time ~(hrs)$'
    fig['layout']['yaxis2']['title'] = '$V_{oc} ~(V)$'

    fig['layout']['xaxis3']['title'] = '$Time ~(hrs)$'
    fig['layout']['yaxis3']['title'] = '$Fill Factor$'

    fig['layout']['xaxis4']['title'] = '$Time ~(hrs)$'
    fig['layout']['yaxis4']['title'] = '$P_{max}$'

    fig.update_layout(legend_tracegroupgap=0)

    return fig
