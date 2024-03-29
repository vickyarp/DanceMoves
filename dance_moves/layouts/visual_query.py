import dash_player
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from app import app
from settings import DATASET_VIDEOS
from layouts.visual_query_layout import visual_query_layout

page_3_layout = html.Div([
    html.A(html.Img(src=app.get_asset_url('logo.png'), style={'width': '300px', 'position': 'fixed','top': '-85px','left': '-40px'}), href="/"),
    dcc.Location(id='url', refresh=False, pathname='/page-3'),
    html.H1('Visual query', style={'text-align': 'center', 'padding-top': '3rem', 'margin-bottom': '3rem'}),
    html.Br(),
    html.Div([
        dcc.Link(dbc.Button('Interact with one video', size="lg"), href="/page-1"),
        dcc.Link(dbc.Button('Interact with two videos and find similarity', size="lg"), href="/page-2"),

    ], style={'display': 'flex', 'justify-content': 'center'}),

    dbc.Row([
        html.Div(
            style={
                'width': '19%',
                'float': 'left',
                'margin': '1% 0% 2% 1%'
            },
            children=[
                dcc.Store(id='memory-output1_b'),
                dcc.Store(id='memory-table_b'),
                dcc.Store(id='current-time1_b'),
                dcc.Store(id='memory-frame_b'),
                dcc.Store(id='selected-row-state'),
                dcc.Store(id='selected-points-state_b'),

                dbc.Card(
                    dbc.CardBody([
                        html.P("Choose Main Video:"),
                        dcc.Dropdown(
                            id='memory-video1_b',
                            options=[{'value': x, 'label': x} for x in DATASET_VIDEOS],
                            value='LU_S_big'
                        ),

                        dash_player.DashPlayer(
                            id='video-player_b',
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
                            max=5,
                            step=0.001,
                            value=[0, 3],
                            updatemode='drag',
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
                        id='graph-im1_b',
                        figure=go.Figure(),
                    ),
                ],
                className="mb-3",),

                html.Div(
                    children=[dbc.Button("Update", id="update-selection_b", style={'margin': '5px'}),
                              dbc.Button("Reset", id="reset-selection_b", style={'margin': '5px'})],
                    style={'display': 'none'}
                ),
            ]
        ),
        visual_query_layout()

    ]),

    html.Br(),
    html.P(u"\u00A9" + ' Master Project of University of Zurich- Vasiliki Arpatzoglou & Artemis Kardara'
           , style={'text-align': 'center', 'fontSize': 16})
],style={'background-image': 'url("/assets/background2.png")'})
