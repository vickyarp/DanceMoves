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
from utils import COLORS, PAIRS_RENDER, DATASET_VIDEOS, BODYPART_THUMBS, POSES_DICT, BODYPART_INDEX_CANONICAL
from keypoint_frames import get_keypoints
from keypoint_frames import create_df
from overall_video_similarity import create_angles, overall_similarity
from heatmap_table_format import heatmap_table_format, highlight_current_frame, tooltip_angles



from app import app
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


page_1_layout = html.Div([
    dcc.Location(id='url',refresh=False,pathname='/page-1'),
    html.H1('Interact with one video', style={'text-align': 'center'}),
    html.Br(),
    html.Div([
        dcc.Link(dbc.Button('Go back to home page', size="lg"), href="/"),
        dcc.Link(dbc.Button('Interact with two videos and find similarity', size="lg"), href="/page-2"),
        dcc.Link(dbc.Button('Interact with visual query', size="lg"), href="/page-3"),
        ],style={ 'display': 'flex', 'justify-content': 'center'}),

    dbc.Row([
        html.Div(
            style={
                'width': '20%',
                'float': 'left',
                'margin': '1% 2% 2% 1%'
            },
            children=[
                dcc.Store(id='memory-output1_b'),
                dcc.Store(id='memory-table_b'),
                dcc.Store(id='current-time1_b'),
                dcc.Store(id='memory-frame_b'),

                # dcc.Input(
                #     id='input-url',
                #     value='/assets/TB_F_FB.mp4'
                # ),
                # html.Button('Change video', id='button-update-url'),
                dbc.Card(
                    dbc.CardBody([
                        html.P("Choose Main Video:"),
                        dcc.Dropdown(
                            id='memory-video1_b',
                            options=[{'value': x, 'label': x} for x in DATASET_VIDEOS],
                            value='BA_R_WA'
                        ),

                        dash_player.DashPlayer(
                            id='video-player_b',
                            # url='/assets/TB_F_FB.mp4',#t=npt:2.3,2.9',
                            currentTime=0,
                            controls=True,
                            intervalCurrentTime=40,
                            loop=True,
                            width='100%',
                            height='min-content'
                        ),
                        html.Div(
                            id='div-current-time_b',
                            style={'margin': '10px 0px'}
                        ),
                        html.Div(
                            id='div-method-output_b',
                            style={'margin': '10px 0px'}
                        ),
                    ]),
                    className="mb-3",
                ),

                dbc.Card([
                    dbc.CardHeader([
                        dcc.Checklist(
                            id='radio-bool-props_b',
                            options=[{'label': val.capitalize(), 'value': val} for val in [
                                'playing',
                                'loop',
                                'controls',
                                'muted'
                            ]],
                            value=['loop', 'muted']
                        ),

                        html.P("Playback Range: {}", id='output-container-range-slider_b'),
                        dcc.RangeSlider(
                            id='range-slider_b',
                            min=0,
                            max=DURATION,
                            step=0.001,
                            value=[0, 3],
                            updatemode='drag',
                            # marks={i: "%g" %i for i in np.arange(0, 10, 0.1)},
                        ),

                        html.P("Playback Rate:", ),
                        dcc.Slider(
                            id='slider-playback-rate_b',
                            min=0,
                            max=1.5,
                            step=None,
                            updatemode='drag',
                            marks={i: str(i) + 'x' for i in
                                   [0, 0.25, 0.5, 0.75, 1, 1.5]},
                            value=0.25
                        ),
                    ]),
                ],
                    className="mb-3", )
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
                dcc.Tabs(id='table-tabs_b', value='tab-2', children=[
                    dcc.Tab(label='Frame Level', value='tab-1'),
                    dcc.Tab(label='Video Level', value='tab-2'),
                ]),
                html.Div(id='tabs-content_b'),
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
                id = 'graph-im1_b',
                style={'height': '50vh'}
            ),
        ]
    ),
]),
    html.Br(),
    html.P(u"\u00A9" + ' Master Project of University of Zurich- Vasiliki Arpatzoglou & Artemis Kardara'
           , style={'text-align': 'center', 'fontSize': 16})
])


@app.callback([Output('memory-table_b', 'data'),
               Output('memory-output1_b', 'data'),
               Output('video-player_b', 'url'),
               Output('video-player_b', 'duration')],
              Input('memory-video1_b', 'value'))
def get_dataframes(video_selected1):
    if not video_selected1 :
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    url1 = '/assets/{}.mp4'.format(video_selected1)
    duration = 5 ##################################################### TODO
    df_angles = create_df(video_selected1)
    df_angles.insert(0, 'angles', BODYPART_THUMBS, True)
    # df_angles = df_angles.loc[BODYPART_INDEX_CANONICAL, :]
    keypoints1 = get_keypoints(video_selected1)
    data = []
    for frame in keypoints1:
        df = create_coordinate_df(frame)
        data.append(df.to_json())


    angles1 = create_angles(video_selected1).T.fillna(0)
    #return df_angles.to_json(), data, url1, data2, url2, duration, similarity
    return df_angles.to_json(), data, url1, duration


@app.callback(Output('video-player_b', 'playing'),
              Input('radio-bool-props_b', 'value'))
def update_prop_playing(values):
    return 'playing' in values


@app.callback(Output('video-player_b', 'loop'),
              Input('radio-bool-props_b', 'value'))
def update_prop_loop(values):
    return 'loop' in values


@app.callback(
    [Output('output-container-range-slider_b', 'children'),
     Output('range-slider_b', 'max')],
    [Input('range-slider_b', 'value'),
     Input('video-player_b', 'duration')])
def update_output(value, duration):
    if duration:
        return 'Playback range: "{}"'.format(value), duration
    else:
        return 'Playback range: "{}"'.format(value), dash.no_update


@app.callback(Output('memory-frame_b', 'data'),
              Input('video-player_b', 'currentTime'))
def update_current_frame(currentTime):
    try:
        frame_no = int(np.round(currentTime / .04))
        return frame_no
    except:
        return 0


@app.callback(Output('video-player_b', 'seekTo'),
              Input('video-player_b', 'currentTime'),
             [State('range-slider_b', 'value'),
              State('video-player_b', 'duration')])
def update_position(currentTime, value, duration):
    start = list(value)[0]
    end = list(value)[1]
    if currentTime and currentTime >= end:
        if currentTime > 1:
            return start
        else:
            percentage = (start / duration)
            return percentage
            # return 0, 0
    else:
        return dash.no_update


@app.callback(Output('tabs-content_b', 'children'),
              [Input('table-tabs_b', 'value'),
               Input('memory-output1_b', 'data'),
               Input('memory-table_b', 'data'),
               Input('video-player_b', 'playing')],
               State('video-player_b', 'currentTime'))
def render_content(tab, dft, df_angles, playing, currentTime):
    try:
        frame_no = int(np.round(currentTime / .04))

        if tab == 'tab-1':
            df = dft[int(np.round(currentTime / .04))]
            df = pd.read_json(df)
            return [html.Div([
                html.H4('Frame #{}'.format(frame_no)),
                dash_table.DataTable(
                    id='table-tab1_b',
                    columns=[{"name": i, "id": i, 'type': 'numeric', 'format': Format(precision=2, scheme=Scheme.fixed),} for i in df.columns],
                    data=df.to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                )
            ])]
        elif tab == 'tab-2':
            df_angles = pd.read_json(df_angles)
            return render_datatable(df_angles, frame_no), modal(df_angles, frame_no),
    except:
        return dash.no_update


@app.callback(Output('graph-im1_b', 'figure'),
              Input('video-player_b', 'playing'),
              [State('video-player_b', 'currentTime'),
               State('memory-output1_b', 'data')])
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

            if x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0:
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
    else:
        return dash.no_update


@app.callback(Output('video-player_b', 'controls'),
              Input('radio-bool-props_b', 'value'))
def update_prop_controls(values):
    return 'controls' in values


#
# @app.callback(Output('video-player', 'url'),
#               [Input('button-update-url', 'n_clicks')],
#               [State('input-url', 'value')])
# def update_url(n_clicks, value):
#     return value


@app.callback(Output('video-player_b', 'playbackRate'),
              Input('slider-playback-rate_b', 'value'))
def update_playbackRate(value):
    return value


# Instance Methods
@app.callback(Output('div-current-time_b', 'children'),
              Input('video-player_b', 'currentTime'))
def update_time(currentTime):
    return 'Current Time: {}'.format(currentTime)


@app.callback(Output('div-method-output_b', 'children'),
              Input('video-player_b', 'secondsLoaded'),
              State('video-player_b', 'duration'))
def update_methods(secondsLoaded, duration):
    return 'Second Loaded: {}, Duration: {}'.format(secondsLoaded, duration)


