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
    dcc.Link(dbc.Button('Go back to home page', size="lg"), href="/"),

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
                dcc.Store(id='memory-frame'),
                dcc.Store(id='selected-row-state'),
                dcc.Store(id='selected-points-state'),

                # dcc.Input(
                #     id='input-url',
                #     value='/assets/TB_F_FB.mp4'
                # ),
                # html.Button('Change video', id='button-update-url'),
                dbc.Card(
                    dbc.CardBody([
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
                            width='100%',
                            height='min-content'
                        ),
                        html.Div(
                            id='div-current-time',
                            style={'margin': '10px 0px'}
                        ),
                        html.Div(
                            id='div-method-output',
                            style={'margin': '10px 0px'}
                        ),
                    ]),
                    className="mb-3",
                ),

                dbc.Card([
                    dbc.CardHeader([
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

                        html.P("Playback Rate:",),
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
                    ]),
                ],
                className="mb-3",),
                dbc.Card([
                    dcc.Graph(
                        id = 'graph-im1',
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
