import dash_player
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_reusable_components as drc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
from dash_table.Format import Format, Scheme
import plotly.graph_objects as go

import numpy as np
import pandas as pd
from datatable import render_datatable
from modal import modal
from secondPage import secondPage
from utils import COLORS, PAIRS_RENDER, DATASET_VIDEOS, BODYPART_THUMBS, POSES_DICT
from keypoint_frames import get_keypoints
from keypoint_frames import create_df
from overall_video_similarity import create_angles, overall_similarity, pose_query
from heatmap_table_format import heatmap_table_format, highlight_current_frame, tooltip_angles
from clustering2 import get_dendogram

# app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True
app.title= 'Updating...'
update_title=None
DURATION = 4.105

def get_coordinates(points_with_confidence):
    # points_with_confidence = keypoints[i]
    mask = np.ones(points_with_confidence.size, dtype=bool)
    mask[2::3] = 0
    points = points_with_confidence[mask]
    return points

def create_coordinate_df(points_with_confidence):
    df = pd.DataFrame(columns=['x', 'y', 'confidence'])
    for i, col in enumerate(df.columns):
        mask = np.zeros(points_with_confidence.size, dtype=bool)
        mask[i::3] = 1
        df.iloc[:,i] = pd.Series(points_with_confidence[mask])
    return df



# keypoints = get_keypoints('TB_F_FB')
# video_frames = []
# for frame in keypoints:
#     df = create_coordinate_df(frame)
#     video_frames.append(df)

app.layout = html.Div([
    html.H2('Visual Analysis of Dance Moves', style={'text-align': 'center'}),
    dbc.Row([
    html.Div(
        style={
            'width': '20%',
            'float': 'left',
            'margin': '1% 2% 2% 1%'
        },
        children=[
            dcc.Store(id='memory-output1'),
            dcc.Store(id='memory-output2'),
            dcc.Store(id='memory-table'),
            dcc.Store(id='current-time1'),
            dcc.Store(id='current-time2'),

            # dcc.Input(
            #     id='input-url',
            #     value='/assets/TB_F_FB.mp4'
            # ),
            # html.Button('Change video', id='button-update-url'),
            html.P("Choose Main Video:"),
            dcc.Dropdown(
                id='memory-video1',
                options=[{'value': x, 'label': x} for x in DATASET_VIDEOS],
                value='BA_R_WA'
            ),

            dash_player.DashPlayer(
                id='video-player',
                #url='/assets/TB_F_FB.mp4',#t=npt:2.3,2.9',
                currentTime= 0,
                controls=True,
                intervalCurrentTime=40,
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

            dcc.Checklist(
                id='radio-bool-props',
                options=[{'label': val.capitalize(), 'value': val} for val in [
                    'playing',
                    'loop',
                    'controls',
                    'muted'
                ]],
                value=['loop', 'muted']
            ),

            html.P("Playback Range: {}", id='output-container-range-slider'),
            dcc.RangeSlider(
                id='range-slider',
                min=0,
                max=DURATION,
                step=0.001,
                value=[0, 3],
                updatemode='drag',
                # marks={i: "%g" %i for i in np.arange(0, 10, 0.1)},
            ),


            html.P("Playback Rate:", style={'margin-top': '20px'}),
            dcc.Slider(
                id='slider-playback-rate',
                min=0,
                max=1.5,
                step=None,
                updatemode='drag',
                marks={i: str(i) + 'x' for i in
                       [0, 0.25, 0.5, 0.75, 1, 1.5]},
                value=0.25
            ),

            # html.P("Update Interval for Current Time:", style={'margin-top': '30px'}),
            # dcc.Slider(
            #     id='slider-intervalCurrentTime',
            #     min=40,
            #     max=1000,
            #     step=None,
            #     updatemode='drag',
            #     marks={i: str(i) for i in [40, 100, 200, 500, 1000]},
            #     value=100,
            # ),

            html.P("Choose Second Video:", style={'margin-top': '40px'}),
            dcc.Dropdown(
                id='memory-video2',
                options=[{'value': x, 'label': x} for x in DATASET_VIDEOS],
                value='BA_R_NA'
            ),
            dash_player.DashPlayer(
                id='video-player2',
                #url='/assets/TB_F_FB.mp4',#t=npt:2.3,2.9',
                currentTime= 0,
                intervalCurrentTime = 100,
                loop=True,
                controls=True,
                width='100%'
            ),
            html.Div(
                id='div-current-time2',
                style={'margin': '10px 0px'}
            ),
            # dcc.Markdown(dedent('''
            # ### Video Examples
            # * mp4: http://media.w3.org/2010/05/bunny/movie.mp4
            # * mp3: https://media.w3.org/2010/07/bunny/04-Death_Becomes_Fur.mp3
            # * webm: https://media.w3.org/2010/05/sintel/trailer.webm
            # * ogv: http://media.w3.org/2010/05/bunny/movie.ogv
            # * Youtube: https://www.youtube.com/watch?v=sea2K4AuPOk
            # '''))
        ]

    ),

    html.Div(
        style={
            'width': '47%',
            'float': 'left',
            'margin': '2% 0% 0% 1%'
        },
        children=[
            html.Div(style={'min-height': '70vh'}, children=[
                dcc.Tabs(id='table-tabs', value='tab-2', children=[
                    dcc.Tab(label='Frame Level', value='tab-1'),
                    dcc.Tab(label='Video Level', value='tab-2'),
                    dcc.Tab(label='Dataset level', value='tab-3'),
                ]),
                html.Div(id='tabs-content'),
            ]),
            drc.Card([
                html.H3(children=[
                    'Overall similarity',
                    dcc.Input(
                        id='overall_similarity',
                        type='text',
                        value='',
                        readOnly=True
                    ),
                ])
            ]),
        ]
    ),
    html.Div(
        style={
            'width': '29%',
            'float': 'right',
            'margin': '-1% 0% 0% 0%'

        },
        children=[

            dcc.Graph(
                id = 'graph-im1',
                style={'height': '50vh'}
            ),
            dcc.Graph(
                id = 'graph-im2',
                style={'height': '50vh'}
            ),
        ]
    ),
]),
secondPage()
])

@app.callback([Output('memory-table', 'data'),
               Output('memory-output1', 'data'),
               Output('video-player', 'url'),
               Output('memory-output2', 'data'),
               Output('video-player2', 'url'),
               Output('video-player', 'duration'),
               Output('overall_similarity', 'value')],
              [Input('memory-video1', 'value'),
               Input('memory-video2', 'value')])
def get_dataframes(video_selected1, video_selected2):
    if not video_selected1 or not video_selected2:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    url1 = '/assets/{}.mp4'.format(video_selected1)
    url2 = '/assets/{}.mp4'.format(video_selected2)
    duration = 5 ##################################################### TODO
    df_angles = create_df(video_selected1)
    df_angles.insert(0, 'angles', BODYPART_THUMBS, True)
    keypoints1 = get_keypoints(video_selected1)
    data = []
    for frame in keypoints1:
        df = create_coordinate_df(frame)
        data.append(df.to_json())
    data2 = []
    keypoints2 = get_keypoints(video_selected2)
    for frame in keypoints2:
        df = create_coordinate_df(frame)
        data2.append(df.to_json())

    angles1 = create_angles(video_selected1).T.fillna(0)
    angles2 = create_angles(video_selected2).T.fillna(0)
    similarity = overall_similarity(angles1, angles2)
    return df_angles.to_json(), data, url1, data2, url2, duration, similarity

@app.callback([Output('video-player', 'playing'),
               Output('video-player2', 'playing')],
              [Input('radio-bool-props', 'value')])
def update_prop_playing(values):
    return 'playing' in values, 'playing' in values


@app.callback([Output('video-player', 'loop'),
               Output('video-player2', 'loop')],
              [Input('radio-bool-props', 'value')])
def update_prop_loop(values):
    return 'loop' in values, 'loop' in values


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
              [Input('video-player', 'currentTime'),
              ],# Input('range-slider', 'value')],
             [State('range-slider', 'value'),
               State('video-player2', 'currentTime'),
              State('video-player', 'duration')])
def update_position(currentTime, value, currentTime2, duration):
    start = list(value)[0]
    end = list(value)[1]
    if currentTime and currentTime >= end:
        if currentTime > 1:
            return start, start
        else:
            return 0, 0
    else:
        return dash.no_update, dash.no_update

# @app.callback(Output('table', 'data'),
#               [Input('video-player', 'playing')],
#               [State('video-player', 'currentTime'),
#                State('memory-output1', 'data')])
# def update_table(playing, currentTime, video_frames):
#     if not playing and currentTime and currentTime > 0:
#         df1 = pd.read_json(video_frames[int(np.round(currentTime / .04))])
#         return df1.to_dict('records')
#
#         # return [{"name": i, "id": i} for i in df1.columns]
#     else: return dash.no_update

@app.callback(Output('tabs-content', 'children'),
              [Input('table-tabs', 'value'),
               Input('memory-output1', 'data'),
               Input('memory-table', 'data'),
               Input('video-player', 'playing')],
               [State('video-player', 'currentTime')])
def render_content(tab, dft, df_angles, playing, currentTime):
    try:
        frame_no = int(np.round(currentTime / .04))

        if tab == 'tab-1':
            df = dft[int(np.round(currentTime / .04))]
            df = pd.read_json(df)
            return [html.Div([
                html.H4('Frame #{}'.format(frame_no)),
                dash_table.DataTable(
                    id='table-tab1',
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                )
            ])]
        elif tab == 'tab-2':
            df_angles = pd.read_json(df_angles)
            return render_datatable(df_angles, frame_no), modal(df_angles, frame_no),

        elif tab == 'tab-3':
            return html.Div(
                dcc.Graph(
                    id='graph-dendro',
                    figure = get_dendogram(),
                    style={'min-width': '100vh'},
                ),
            )


    except:
        return dash.no_update


@app.callback(Output('graph-im1', 'figure'),
              [Input('video-player', 'playing')],
              [State('video-player', 'currentTime'),
               State('memory-output1', 'data')])
def update_figure(playing, currentTime, video_frames):
    if not playing and currentTime and currentTime > 0:

        # points = get_coordinates(keypoints[int(np.round(1/.04))])
        df = pd.read_json(video_frames[int(np.round(currentTime/.04))])
        fig = go.Figure()
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
        for pair, color in zip(PAIRS_RENDER, COLORS):
            x1 = int(df.x[pair[0]])
            y1 = int(df.y[pair[0]])
            x2 = int(df.x[pair[1]])
            y2 = int(df.y[pair[1]])
            z1 = df.confidence[pair[0]]
            z2 = df.confidence[pair[1]]

            if (x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0):
                fig.add_shape(
                    type='line', xref='x', yref='y',
                    x0=x1, x1=x2, y0=y1, y1=y2, line_color=color, line_width=4
                )
            fig.add_shape(
                type='circle', xref='x', yref='y',
                x0=x1 - 3, y0=y1 - 3, x1=x1 + 3, y1=y1 + 3, line_color=color, fillcolor=color
            )
            fig.add_shape(
                type='circle', xref='x', yref='y',
                x0=x2 - 3, y0=y2 - 3, x1=x2 + 3, y1=y2 + 3, line_color=color, fillcolor=color
            )
            fig.add_trace(
                go.Scatter(
                    x=[x2],
                    y=[y2],
                    # mode='markers',
                    # marker_size=8,
                    showlegend=False,
                    marker_color=color,
                    name='',
                    text='Confidence:{:.2f}'.format(z1),
                    opacity=0
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=[x2],
                    y=[y2],
                    showlegend=False,
                    marker_color=color,
                    name='',
                    text='Confidence:{:.2f}'.format(z2),
                    opacity=0
                )
            )


        return fig
    else: return dash.no_update


@app.callback(Output('graph-im2', 'figure'),
              [Input('video-player2', 'playing')],
              [State('video-player2', 'currentTime'),
               State('memory-output2', 'data')])
def update_figure(playing, currentTime, video_frames):
    try:
        if not playing:
            # points = get_coordinates(keypoints[int(np.round(1/.04))])
            df = pd.read_json(video_frames[int(np.round(currentTime / .04))])
            fig = go.Figure()
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
            for pair, color in zip(PAIRS_RENDER, COLORS):
                x1 = int(df.x[pair[0]])
                y1 = int(df.y[pair[0]])
                x2 = int(df.x[pair[1]])
                y2 = int(df.y[pair[1]])
                if (x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0):
                    fig.add_shape(
                        type='line', xref='x', yref='y',
                        x0=x1, x1=x2, y0=y1, y1=y2, line_color=color, line_width=4
                    )
                fig.add_shape(
                    type='circle', xref='x', yref='y',
                    x0=x1 - 3, y0=y1 - 3, x1=x1 + 3, y1=y1 + 3, line_color=color, fillcolor=color
                )
                fig.add_shape(
                    type='circle', xref='x', yref='y',
                    x0=x2 - 3, y0=y2 - 3, x1=x2 + 3, y1=y2 + 3, line_color=color, fillcolor=color
                )
            return fig
    except:
        return dash.no_update
    return dash.no_update


@app.callback([Output('video-player', 'controls'),
               Output('video-player2', 'controls')],
              [Input('radio-bool-props', 'value')])
def update_prop_controls(values):
    return 'controls' in values, 'controls' in values


#
# @app.callback(Output('video-player', 'url'),
#               [Input('button-update-url', 'n_clicks')],
#               [State('input-url', 'value')])
# def update_url(n_clicks, value):
#     return value


@app.callback([Output('video-player', 'playbackRate'),
              Output('video-player2', 'playbackRate')],
              [Input('slider-playback-rate', 'value')])
def update_playbackRate(value):
    return value, value


# Instance Methods
@app.callback([Output('div-current-time', 'children'),
               Output('div-current-time2', 'children')],
              [Input('video-player', 'currentTime'),
               Input('video-player2', 'currentTime')])
def update_time(currentTime, currentTime2):
    return 'Current Time: {}'.format(currentTime), 'Current Time: {}'.format(currentTime2)


@app.callback(Output('div-method-output', 'children'),
              [Input('video-player', 'secondsLoaded')],
              [State('video-player', 'duration')])
def update_methods(secondsLoaded, duration):
    return 'Second Loaded: {}, Duration: {}'.format(secondsLoaded, duration)


# @app.callback(Output('video-player', 'intervalCurrentTime'),
#               [Input('slider-intervalCurrentTime', 'value')])
# def update_intervalCurrentTime(value):
#     return value
#
#
# @app.callback(Output('video-player', 'intervalSecondsLoaded'),
#               [Input('slider-intervalSecondsLoaded', 'value')])
# def update_intervalSecondsLoaded(value):
#     return value
#
#
# @app.callback(Output('video-player', 'intervalDuration'),
#               [Input('slider-intervalDuration', 'value')])
# def update_intervalDuration(value):
#     return value


# @app.callback(Output('video-player', 'seekTo'),
#               [Input('slider-seek-to', 'value')])
# def set_seekTo(value):
#     return value
#
# @app.callback(Output('video-player', 'duration'),
#                 [Input('slider-duration', 'value')])
# def set_durationTo(value):
#     return value

@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

### Search Query callbacks
@app.callback(Output('dif-table', 'children'),
              [Input('memory-video1', 'value'),
               Input('qsearch-1', 'n_clicks'),
               Input('qsearch-2', 'n_clicks'),
               Input('qsearch-3', 'n_clicks')],
              )
def render_dif_table(value, click1, click2, click3):
    # if not click1 or not click2 or not click3 or not value:
    #     return dash.no_update
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)
    if 'qsearch-1' in changed_id:
        pose = POSES_DICT['qsearch-1']['data']
    elif 'qsearch-2' in changed_id:
        pose = POSES_DICT['qsearch-2']['data']
    elif 'qsearch-3' in changed_id:
            pose = POSES_DICT['qsearch-3']['data']
    else: return dash.no_update

    df_angles_dif = pose_query(value, pose)
    df_angles_dif.insert(0, 'angles', BODYPART_THUMBS, True)
    return render_datatable(df_angles_dif, pagesize=12, dif_table='true')


# @app.callback(Output('dif-table', 'children[0]'),
#               [Input('memory-video1', 'value'),
#                Input('qsearch-2', 'n_clicks')],
#               )
# def render_dif_table(value, click):
#     if not click or not value:
#         return dash.no_update
#     else:
#         pose = POSES_DICT['qsearch-2']['data']
#         df_angles_dif = pose_query(value, pose)
#         df_angles_dif.insert(0, 'angles', BODYPART_THUMBS, True)
#         return render_datatable(df_angles_dif, pagesize=12)
#
# @app.callback(Output('dif-table', 'children[1]'),
#               [Input('memory-video1', 'value'),
#                Input('qsearch-3', 'n_clicks')],
#               )
# def render_dif_table(value, click):
#     if not click or not value:
#         return dash.no_update
#     else:
#         pose = POSES_DICT['qsearch-3']['data']
#         df_angles_dif = pose_query(value, pose)
#         df_angles_dif.insert(0, 'angles', BODYPART_THUMBS, True)
#         return render_datatable(df_angles_dif, pagesize=12)

if __name__ == '__main__':
    app.run_server(debug=True)
