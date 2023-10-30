import plotly.express as px

from plotly.subplots import make_subplots
import plotly.graph_objects as go

from matplotlib import colors

def plot_with_margin(data_frame, x: str, y: str, color: str, palette: dict, error: str=None, upper_bound: str=None, lower_bound: str=None, title: str='Continuous'):

    if (type(error)!=str):
        if ((type(upper_bound)!=str) or (type(lower_bound)!=str)):
            print("No error and no bound parameters, you can use px.line")
            return False
    else:
        lower_bound='lower_bound'
        data_frame[lower_bound] = data_frame[y] - data_frame[error]
        upper_bound='upper_bound'
        data_frame[upper_bound] = data_frame[y] + data_frame[error]

    colorss = set(data_frame[color])

    if (colorss != set(palette.keys())):
        print(f"The {color} column and the keys of palette are not same")
        return False

    go_scatters = []

    for colour in colorss:
        if palette[colour][:3]=='rgb':
            fillcolour = 'rgba' + palette[colour][3:-1] + ', 0.3)'
        else:
            # print(palette[colour])
            fillcolour = colors.to_rgb(palette[colour])
            fillcolour = (int(fillcolour[0]), int(fillcolour[1]), int(fillcolour[2]), 0.3)
            fillcolour = 'rgba' + str(fillcolour)
            
        tmp_df = data_frame[data_frame[color]==colour]

        go_scatters.append(
            go.Scatter(
                name=str(colour), x=tmp_df[x], y=tmp_df[y], mode='lines',
                line=dict(color=palette[colour])
            ))
        go_scatters.append(
            go.Scatter(x=tmp_df[x]+tmp_df[x][::-1], # x, then x reversed
                       y=tmp_df[upper_bound]+tmp_df[lower_bound][::-1], # upper, then lower reversed
                       fill='toself', fillcolor=fillcolour, line=dict(color='rgba(255,255,255,0)'), showlegend=False
            ))
        # go_scatters.append(
        #     go.Scatter(
        #         name='Upper Bound', x=tmp_df[x], y=tmp_df[upper_bound], mode='lines',
        #         marker=dict(color=fillcolour), line=dict(width=0), showlegend=False
        #     ))
        # go_scatters.append(
        #     go.Scatter(
        #         name='Lower Bound', x=tmp_df[x], y=tmp_df[lower_bound], mode='lines',
        #         marker=dict(color=fillcolour), line=dict(width=0), fillcolor=fillcolour,
        #         fill='tonexty', showlegend=False
        #     ))

    fig = go.Figure(go_scatters)
    fig.update_layout(
        yaxis_title=y,
        title=title)
    
    return fig
