from plotly.subplots import make_subplots
import plotly.graph_objects as go


def four_subplots_prepper(subplots_titles=("A", "B", "C", "D")) -> go.Figure:
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=subplots_titles,
        horizontal_spacing=0.05,
        vertical_spacing=0.125
    )

    # edit axis labels
    fig['layout']['xaxis']['title'] = '$Time ~(hrs)$'
    fig['layout']['yaxis']['title'] = '$I_{sc} ~(A)$'

    fig['layout']['xaxis2']['title'] = '$Time ~(hrs)$'
    fig['layout']['yaxis2']['title'] = '$V_{oc} ~(V)$'

    fig['layout']['xaxis3']['title'] = '$Time ~(hrs)$'
    fig['layout']['yaxis3']['title'] = '$Fill ~Factor$'

    fig['layout']['xaxis4']['title'] = '$Time ~(hrs)$'
    fig['layout']['yaxis4']['title'] = '$P_{max}$'

    # FIXME: hoverformat needs to be reset to default
    yaxis_format = dict(
            tickformat=".2s",
            showexponent='all',
            exponentformat='SI',
            hoverformat=''
        )
    fig.update_layout(
        legend_tracegroupgap=0,
        yaxis=yaxis_format,
        yaxis2=yaxis_format,
        yaxis3=yaxis_format,
        yaxis4=yaxis_format
    )

    return fig
