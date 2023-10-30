import plotly.express as px

from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_with_margin(data_frame, x: str, y: str, color: str, palette: dict, error: str=None, upper_bound: str=None, lower_bound: str=None):

    if (type(error)!=str):
        if ((type(upper_bound)!=str) or (type(lower_bound)!=str)):
            print("No error and no bound parameters, you can use px.line")
            return False
    else:
        lower_bound='lower_bound'
        data_frame[lower_bound] = data_frame[y] - data_frame[error]/2
        upper_bound='upper_bound'
        data_frame[upper_bound] = data_frame[y] + data_frame[error]/2

    colors = set(data_frame[color])

    if (colors != set(palette.keys())):
        print(f"The {color} column and the keys of palette are not same")
        return False

    go_scatters = []

    for colour in colors:
        if colour[:3]=='rgb':
            fillcolour = 'rgba' + colour[3:-1] + ', 0.3)'

        go_scatters.append(
            go.Scatter(
                name=str(colour), x=data_frame[x], y=data_frame[y], mode='lines',
                line=dict(color=palette[colour])
            ))
        go_scatters.append(
            go.Scatter(
                name='Upper Bound', x=data_frame[x], y=data_frame[upper_bound], mode='lines',
                marker=dict(color="#444"), line=dict(width=0), showlegend=False
            ))
        go_scatters.append(
            go.Scatter(
                name='Lower Bound', x=data_frame[x], y=data_frame[lower_bound], mode='lines',
                marker=dict(color="#444"), line=dict(width=0), fillcolor=fillcolour,
                fill='tonexty', showlegend=False
            ))

    fig = go.Figure(go_scatters)
    fig.update_layout(
        yaxis_title=y,
        title=f"Continuous, {y}")
    
    return fig
