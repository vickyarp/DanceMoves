from textwrap import dedent

import dash_player
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import numpy as np

from utils import COLORS, PAIRS_RENDER
from keypoint_frames import get_keypoints
app = dash.Dash(__name__)
server = app.server

app.scripts.config.serve_locally = True

DURATION = 4.105

# points_with_confidence = np.array(
#     [248.94, 81.6767, 0.935687, 262.687, 118.87, 0.906967, 242.13, 120.828, 0.820844, 207.858, 141.354, 0.815456,
#      166.77, 149.211, 0.860964, 284.162, 116.913, 0.775896, 318.412, 135.519, 0.828298, 350.708, 151.135, 0.871648,
#      266.591, 203.95, 0.656241, 255.806, 203.006, 0.626415, 264.625, 266.586, 0.782925, 293.975, 319.394, 0.833589,
#      277.339, 203.955, 0.642223, 266.581, 269.504, 0.806337, 256.783, 328.197, 0.785736, 246.992, 75.8567, 0.889436,
#      254.819, 75.8395, 0.954964, 0, 0, 0, 270.477, 78.7767, 0.903617, 256.768, 346.795, 0.73078, 261.699, 343.878,
#      0.736936, 255.81, 332.087, 0.689596, 275.393, 326.268, 0.702509, 276.333, 324.268, 0.648877, 300.788, 325.271,
#      0.73803])

def get_coordinates(points_with_confidence):
    # points_with_confidence = keypoints[i]
    mask = np.ones(points_with_confidence.size, dtype=bool)
    mask[2::3] = 0
    points = points_with_confidence[mask]
    return points


def update_stickfigure(points):
    fig = go.Figure()
    # Add image
    img_width = 400
    img_height = 400
    scale_factor = 0.5
    fig.add_layout_image(
        x=100,
        sizex=img_width,
        y=100,
        sizey=img_height + 200,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below"
    )
    fig.update_xaxes(showgrid=False, scaleanchor='y', range=(0, img_width))
    fig.update_yaxes(showgrid=False, range=(img_height, 0))


    # Line shape added programatically
    for pair, color in zip(PAIRS_RENDER, COLORS):
        x1 = int(points[2 * pair[0]])
        y1 = int(points[2 * pair[0] + 1])
        x2 = int(points[2 * pair[1]])
        y2 = int(points[2 * pair[1] + 1])
        if (x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0):
            # cv2.line(img, (x1, y1), (x2, y2), color, thickness=4)
            # cv2.circle(img, (x1, y1), 5, color, -1)
            fig.add_shape(
                type='line', xref='x', yref='y',
                x0=x1, x1=x2, y0=y1, y1=y2, line_color=color, line_width=4
            )
            fig.add_shape(
                type='circle', xref='x', yref='y',
                x0=x1-3, y0=y1-3, x1=x1+3, y1=y1+3, line_color=color, fillcolor=color
            )
    return fig

keypoints = get_keypoints('TB_F_FB')
# fig = update_stickfigure(get_coordinates(keypoints[1]))
#fig = go.Figure()
# Add image
# img_width = 400
# img_height = 400
# scale_factor = 0.5
# fig.add_layout_image(
#         x=100,
#         sizex=img_width,
#         y=100,
#         sizey=img_height+200,
#         xref="x",
#         yref="y",
#         opacity=1.0,
#         layer="below"
# )
# fig.update_xaxes(showgrid=False, scaleanchor='y',range=(0, img_width))
# fig.update_yaxes(showgrid=False,  range=(img_height, 0))

app.layout = html.Div([
    html.Div(
        style={
            'width': '30%',
            'float': 'left',
            'margin': '0% 5% 1% 5%'
        },
        children=[
            dash_player.DashPlayer(
                id='video-player',
                url='/assets/TB_F_FB.mp4',#t=npt:2.3,2.9',
                currentTime= 0,
                controls=True,
                loop=True,
                width='100%'
            ),
            html.Div(
                id='div-current-time',
                style={'margin': '10px 0px'}
            ),

            html.Div(
                id='div-method-output',
                style={'margin': '10px 0px'}
            ),
            dash_player.DashPlayer(
                id='video-player2',
                url='/assets/TB_F_FB.mp4',#t=npt:2.3,2.9',
                currentTime= 0,
                controls=True,
                width='100%'
            ),
            dcc.Markdown(dedent('''
            ### Video Examples
            * mp4: http://media.w3.org/2010/05/bunny/movie.mp4
            * mp3: https://media.w3.org/2010/07/bunny/04-Death_Becomes_Fur.mp3
            * webm: https://media.w3.org/2010/05/sintel/trailer.webm
            * ogv: http://media.w3.org/2010/05/bunny/movie.ogv
            * Youtube: https://www.youtube.com/watch?v=sea2K4AuPOk
            '''))
        ]

    ),


    html.Div(
        style={
            'width': '53%',
            'float': 'left'
        },
        children=[

            dcc.Graph(
                id = 'graph-im',
                # figure = fig
            ),

            dcc.Input(
                id='input-url',
                value='/assets/TB_F_FB.mp4'
            ),

            html.Button('Change URL', id='button-update-url'),

            dcc.Checklist(
                id='radio-bool-props',
                options=[{'label': val.capitalize(), 'value': val} for val in [
                    'playing',
                    'loop',
                    'controls',
                    'muted'
                ]],
                value=['controls']
            ),

            html.P("Playback Range: {}", id='output-container-range-slider'),
            dcc.RangeSlider(
                id='range-slider',
                min=0,
                max=DURATION,
                step=0.001,
                value=[0, 1],
                updatemode='mouseup',
                # marks={i: "%g" %i for i in np.arange(0, 10, 0.1)},
            ),


            html.P("Playback Rate:", style={'margin-top': '25px'}),
            dcc.Slider(
                id='slider-playback-rate',
                min=0,
                max=4,
                step=None,
                updatemode='drag',
                marks={i: str(i) + 'x' for i in
                       [0, 0.25, 0.5, 0.75, 1, 2, 3, 4]},
                value=1
            ),

            html.P("Update Interval for Current Time:", style={'margin-top': '30px'}),
            dcc.Slider(
                id='slider-intervalCurrentTime',
                min=40,
                max=1000,
                step=None,
                updatemode='drag',
                marks={i: str(i) for i in [40, 100, 200, 500, 1000]},
                value=100
            ),

            html.P("Update Interval for seconds loaded:", style={'margin-top': '30px'}),
            dcc.Slider(
                id='slider-intervalSecondsLoaded',
                min=200,
                max=2000,
                step=None,
                updatemode='drag',
                marks={i: str(i) for i in [200, 500, 750, 1000, 2000]},
                value=500
            ),

            html.P("Update Interval for duration:",
                   style={'margin-top': '30px'}),
            dcc.Slider(
                id='slider-intervalDuration',
                min=200,
                max=2000,
                step=None,
                updatemode='drag',
                marks={i: str(i) for i in [200, 500, 750, 1000, 2000]},
                value=500
            ),

            html.P("Seek To:", style={'margin-top': '30px'}),
            dcc.Slider(
                id='slider-seek-to',
                min=0,
                max=1,
                step=None,
                updatemode='drag',
                marks={i: str(i * 100) + '%' for i in [0, 0.25, 0.5, 0.75, 1]},
                value=0
            ),

            html.P("Duration", style={'margin-top': '30px'}),
            dcc.Slider(
                id='slider-duration',
                min=0,
                max=4,
                step=100,
                updatemode='drag',
                marks={i: str(i) for i in [0,1,2,3,4]},
                value=0
            ),
        ]
    ),
])


@app.callback([Output('video-player', 'playing'),
               Output('video-player2', 'playing')],
              [Input('radio-bool-props', 'value')])
def update_prop_playing(values):
    return ['playing' in values, 'playing' in values]

#
# @app.callback(Output('video-player', 'loop'),
#               [Input('radio-bool-props', 'value')])
# def update_prop_loop(values):
#     return 'loop' in values


@app.callback(
    [Output('output-container-range-slider', 'children'),
     Output('range-slider', 'max')],
    [Input('range-slider', 'value'),
     Input('video-player', 'duration')])
def update_output(value, duration):
    if duration:
        return 'Playback range: "{}"'.format(value), duration
    else:
        return 'Playback range: "{}"'.format(value), dash.no_update

@app.callback([Output('video-player', 'seekTo'),
               Output('video-player2', 'seekTo')],
              [Input('video-player', 'currentTime')],
              [State('range-slider', 'value'),
               State('video-player2', 'currentTime'),
              State('video-player', 'duration')
               ]# State('video-player', 'url'),
               # State('video-player2', 'url')]
              )              # [State('video-player2', 'currentTime')])
def update_position(currentTime, value, currentTime2, duration):
    start = list(value)[0]
    end = list(value)[1]
    if currentTime and currentTime >= end:
        return start, start
    else:
        return dash.no_update, dash.no_update

@app.callback(Output('graph-im', 'figure'),
              [Input('video-player', 'currentTime')],
              [
               State('video-player', 'playing')])
def update_figure(currentTime, playing):
    if not playing and currentTime and currentTime > 0:
        # points = get_coordinates(keypoints[int(np.round(1/.04))])
        points = get_coordinates(keypoints[int(np.round(currentTime/.04))])
       # return update_stickfigure(points, fig)
        fig = go.Figure()

        # Line shape added programatically
        for pair, color in zip(PAIRS_RENDER, COLORS):
            x1 = int(points[2 * pair[0]])
            y1 = int(points[2 * pair[0] + 1])
            x2 = int(points[2 * pair[1]])
            y2 = int(points[2 * pair[1] + 1])
            if (x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0):
                # cv2.line(img, (x1, y1), (x2, y2), color, thickness=4)
                # cv2.circle(img, (x1, y1), 5, color, -1)
                fig.add_shape(
                    type='line', xref='x', yref='y',
                    x0=x1, x1=x2, y0=y1, y1=y2, line_color=color, line_width=4
                )
                fig.add_shape(
                    type='circle', xref='x', yref='y',
                    x0=x1 - 3, y0=y1 - 3, x1=x1 + 3, y1=y1 + 3, line_color=color, fillcolor=color
                )
        return fig

    else: return dash.no_update

@app.callback(Output('video-player', 'controls'),
              [Input('radio-bool-props', 'value')])
def update_prop_controls(values):
    return 'controls' in values


@app.callback(Output('video-player', 'muted'),
              [Input('radio-bool-props', 'value')])
def update_prop_muted(values):
    return 'muted' in values


# @app.callback(Output('video-player', 'volume'),
#               [Input('slider-volume', 'value')])
# def update_volume(value):
#     return value


@app.callback(Output('video-player', 'url'),
              [Input('button-update-url', 'n_clicks')],
              [State('input-url', 'value')])
def update_url(n_clicks, value):
    return value


@app.callback([Output('video-player', 'playbackRate'),
              Output('video-player2', 'playbackRate')],
              [Input('slider-playback-rate', 'value')])
def update_playbackRate(value):
    return value, value


# Instance Methods
@app.callback(Output('div-current-time', 'children'),
              [Input('video-player', 'currentTime')])
def update_time(currentTime):
    return 'Current Time: {}'.format(currentTime)


@app.callback(Output('div-method-output', 'children'),
              [Input('video-player', 'secondsLoaded')],
              [State('video-player', 'duration')])
def update_methods(secondsLoaded, duration):
    return 'Second Loaded: {}, Duration: {}'.format(secondsLoaded, duration)


@app.callback(Output('video-player', 'intervalCurrentTime'),
              [Input('slider-intervalCurrentTime', 'value')])
def update_intervalCurrentTime(value):
    return value


@app.callback(Output('video-player', 'intervalSecondsLoaded'),
              [Input('slider-intervalSecondsLoaded', 'value')])
def update_intervalSecondsLoaded(value):
    return value


@app.callback(Output('video-player', 'intervalDuration'),
              [Input('slider-intervalDuration', 'value')])
def update_intervalDuration(value):
    return value


# @app.callback(Output('video-player', 'seekTo'),
#               [Input('slider-seek-to', 'value')])
# def set_seekTo(value):
#     return value

@app.callback(Output('video-player', 'duration'),
                [Input('slider-duration', 'value')])
def set_durationTo(value):
    return value


if __name__ == '__main__':
    app.run_server(debug=True)
