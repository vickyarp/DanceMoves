import dash
import dash_player
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_reusable_components as drc
from dash.dependencies import Input, Output, State
from modal import modal

from app import app
from overall_video_similarity import pose_query
from utils import  BODYPART_THUMBS, POSES_DICT, DATASET_VIDEOS
from datatable import render_datatable
from secondPage import secondPage

DURATION = 4.105

page_3_layout = html.Div([
    html.H1('Visual query', style={'text-align': 'center'}),
    html.Br(),
    html.Div([
        dcc.Link(dbc.Button('Go back to home page', size="lg"), href="/"),
        dcc.Link(dbc.Button('Interact with one video', size="lg"), href="/page-1"),
        dcc.Link(dbc.Button('Interact with two videos and find similarity', size="lg"), href="/page-2"),

    ], style={'display': 'flex', 'justify-content': 'center'}),

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
                dcc.Store(id='selected-row-state_b'),
                dcc.Store(id='selected-points-state_b'),

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
                            #url='/assets/TB_F_FB.mp4',#t=npt:2.3,2.9',
                            currentTime= 0,
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

                        html.P("Playback Rate:",),
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
                className="mb-3",),
                dbc.Card([
                    dcc.Graph(
                        id= 'graph-im1_b',
                        style={'height': '50vh'}
                    ),
                ],
                className="mb-3",)
            ]
        ),
        secondPage()

    ]),

    html.Br(),
    html.P(u"\u00A9" + ' Master Project of University of Zurich- Vasiliki Arpatzoglou & Artemis Kardara'
           , style={'text-align': 'center', 'fontSize': 16})
])
