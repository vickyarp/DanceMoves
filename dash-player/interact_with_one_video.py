import dash_player
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_reusable_components as drc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import dash_table
from dash_table.Format import Format, Scheme
import plotly.graph_objects as go

import numpy as np
import pandas as pd
from datatable import render_datatable
from modal import modal
from utils import COLORS, PAIRS_RENDER, DATASET_VIDEOS, BODYPART_THUMBS, POSES_DICT, BODYPART_INDEX_CANONICAL, update_selected_state, angles_to_ids, angle_ids_to_angles
from keypoint_frames import get_keypoints
from keypoint_frames import create_df
from overall_video_similarity import create_angles, overall_similarity
from render_stick_figure import render_stick_figure
from heatmap_table_format import heatmap_table_format, highlight_current_frame, tooltip_angles, Blue, Sand, Else, Green





from app import app
DURATION = 4.105
colormaps = {'Blue': Blue, 'Sand': Sand , 'Else': Else, 'Green': Green}


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
        ], style={ 'display': 'flex', 'justify-content': 'center'}),

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
                dcc.Store(id='selected-row-state'),
                dcc.Store(id='selected-points-state'),
                dcc.Store(id='temp-state_b'),

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
            #'margin': '2% 0% 0% 1%'
            'margin': '1% 2% 2% 1%'
        },
        children=[
            html.Div(style={'min-height': '70vh'}, children=[
                dcc.Tabs(id='table-tabs_b', value='tab-2', children=[
                    dcc.Tab(label='Frame Level', value='tab-1', style={'fontWeight': 'bold', 'height': '5vh'}),
                    dcc.Tab(label='Video Level', value='tab-2', style={'fontWeight': 'bold','height': '5vh'}),
                ]),
                dcc.RadioItems(
                    id='gradient-scheme',
                    options=[
                        {'label': 'Orange to Red', 'value': 'Else'},
                        {'label': 'Sand', 'value': 'Sand'},
                        {'label': 'Light Green to Blue', 'value': 'Blue'},
                        {'label': 'Green', 'value': 'Green'}
                    ],
                    value='Blue',
                    labelStyle={'float': 'right', 'display': 'inline-block', 'margin-right': 10, 'fontWeight': 'bold'}
                ),
                html.Div(id='tabs-content_b'),



            ]),
        ]
    ),
        html.Div(
            style={
                'width': '20%',
                'float': 'right',
                #'margin': '-1% 0% 0% 0%'
                'margin': '1% 2% 2% 1%'

            },
            children=[

                dcc.Graph(
                    id='graph-im1_b',
                    style={'height': '50vh'}
                ),
                html.Div([dbc.Button("Reset", id="reset-selection_b")],
                         style={'display': 'flex', 'justify-content': 'center'}),
            ]
        ),
]),
    html.Br(),
    html.P(u"\u00A9" + ' Master Project of University of Zurich- Vasiliki Arpatzoglou & Artemis Kardara'
           , style={'text-align': 'center', 'fontSize': 16})
], style={'background-image': 'url(https://img.freepik.com/free-vector/3d-perspective-style-diamond-shape-white-background_1017-27556.jpg?size=626&ext=jpg)'})



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
               Input('video-player_b', 'playing'),
               Input('selected-row-state', 'data'),
               Input('gradient-scheme', 'value')],
               [State('video-player_b', 'currentTime')])
def render_content(tab, dft, df_angles, selected_rows, playing, value, currentTime):
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
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    style_table={'overflowX': 'scroll'},
                    style_cell={
                        'backgroundColor': colormaps[value][2],
                        'color': 'black',
                        'fontWeight': 'bold'
                    }
                )
            ])]
        elif tab == 'tab-2':
            df_angles = pd.read_json(df_angles)
            # if value == 'Viridis':
            #      colormap = Viridis
            # elif value == 'Plasma':
            #     colormap = Plasma
            # elif value == 'Else':
            #     colormap = Else
            return render_datatable(df_angles, frame_no, selected_rows=selected_rows,colormap=colormaps[value]), modal(df_angles, frame_no)
    except:
        return dash.no_update


#VICKYYYYYYYYYYYYYYYYYYYY

# @app.callback(Output('graph-im1_b', 'figure'),
#               Input('video-player_b', 'playing'),
#               [State('video-player_b', 'currentTime'),
#                State('memory-output1_b', 'data')])
# def update_figure(playing, currentTime, video_frames):
#     if not playing and currentTime and currentTime > 0:
#
#         # points = get_coordinates(keypoints[int(np.round(1/.04))])
#         df = pd.read_json(video_frames[int(np.round(currentTime/.04))])
#         fig = go.Figure()
#         img_width = 400
#         img_height = 400
#         scale_factor = 0.5
#         fig.add_layout_image(
#             x=100,
#             sizex=img_width,
#             y=100,
#             sizey=img_height + 200,
#             xref="x",
#             yref="y",
#             opacity=1.0,
#             layer="below"
#         )
#         fig.update_xaxes(showgrid=False, scaleanchor='y', range=(0, img_width))
#         fig.update_yaxes(showgrid=False, range=(img_height, 0))
#         for pair, color in zip(PAIRS_RENDER, COLORS):
#             x1 = int(df.x[pair[0]])
#             y1 = int(df.y[pair[0]])
#             x2 = int(df.x[pair[1]])
#             y2 = int(df.y[pair[1]])
#             z1 = df.confidence[pair[0]]
#             z2 = df.confidence[pair[1]]
#
#             if x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0:
#                 fig.add_shape(
#                     type='line', xref='x', yref='y',
#                     x0=x1, x1=x2, y0=y1, y1=y2, line_color=color, line_width=4
#                 )
#             fig.add_shape(
#                 type='circle', xref='x', yref='y',
#                 x0=x1 - 3, y0=y1 - 3, x1=x1 + 3, y1=y1 + 3, line_color=color, fillcolor=color
#             )
#             fig.add_shape(
#                 type='circle', xref='x', yref='y',
#                 x0=x2 - 3, y0=y2 - 3, x1=x2 + 3, y1=y2 + 3, line_color=color, fillcolor=color
#             )
#             fig.add_trace(
#                 go.Scatter(
#                     x=[x2],
#                     y=[y2],
#                     # mode='markers',
#                     # marker_size=8,
#                     showlegend=False,
#                     marker_color=color,
#                     name='',
#                     text='Confidence:{:.2f}'.format(z1),
#                     opacity=0
#                 )
#             )
#             fig.add_trace(
#                 go.Scatter(
#                     x=[x2],
#                     y=[y2],
#                     showlegend=False,
#                     marker_color=color,
#                     name='',
#                     text='Confidence:{:.2f}'.format(z2),
#                     opacity=0
#                 )
#             )
#
#         return fig
#     else:
#         return dash.no_update

@app.callback(Output('graph-im1_b', 'figure'),
              [Input('video-player_b', 'playing'),
               # Input('graph-im1', 'selectedData'),
               # Input('graph-im1', 'clickData'),
               Input('graph-im1_b', 'restyleData'),
               Input('reset-selection_b', 'n_clicks'),
               Input('selected-points-state', 'data')],
              [State('video-player_b', 'currentTime'),
               State('memory-output1_b', 'data'),
               State('memory-video1_b', 'value'),
               State('graph-im1_b', 'figure')])

# def update_figure(playing, selectedData, clickData, restyleData, n_clicks, selected_points, currentTime, video_frames, video1, fig):
def update_figure(playing, restyleData, n_clicks, selected_points, currentTime, video_frames, video1, fig):

    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'video-player_b.playing':
        if not playing and currentTime and currentTime > 0:
            # points = get_coordinates(keypoints[int(np.round(1/.04))])
            df = pd.read_json(video_frames[int(np.round(currentTime/.04))])
            return render_stick_figure(df, video1)

        else: return dash.no_update
    # elif ctx.triggered[0]['prop_id'] == 'reset-selection.n_clicks':
    #     if n_clicks is None:
    #         raise dash.PreventUpdate
    #     else:
    #         default_state = {'angles': [], 'bodyparts': []}
    #         df = pd.read_json(video_frames[int(np.round(currentTime / .04))])
    #         return render_stick_figure(df, video1), default_state
    else:
        try:
            # initialize state
            if selected_points == None : selected_points = {'angles': [], 'bodyparts': []}
            selection = None

            # Update selection based on which event triggered the update.
            trigger = dash.callback_context.triggered[0]['prop_id']
            # print(trigger)
            # if trigger == 'graph-im1.clickData':
            #     selection = [point["curveNumber"] for point in clickData["points"]]
            #     print(selection)
            #     for curve_number in selection:
            #         # fig["data"][curve_number]["selectedpoints"] = selection
            #         fig["data"][curve_number]["line"]["color"] = 'black'
            # if trigger == 'graph-im1.selectedData':
            #     selection = [point["curveNumber"] for point in selectedData["points"]]
            #     selection_names = [fig["data"][curve_number]['name'] for curve_number in selection]
            #
            #     for curve_number in selection:
            #         # fig["data"][curve_number]["selectedpoints"] = selection
            #         fig["data"][curve_number]["line"]["color"] = 'black'
            #     selected_points = update_selected_state(state=selected_points, bodypart_names=selection_names)
            #     return fig

            if trigger == 'graph-im1_b.restyleData':
                print(restyleData)
                # print(selectedData)

            if trigger == 'selected-points-state.data':
                for bodypart in selected_points['bodyparts']:
                    curve = next(filter(lambda x: x['name'] == bodypart,  fig["data"]))
                    curve_number = fig["data"].index(curve)
                    fig["data"][curve_number]["line"]["color"] = 'black'
            # fig["data"][0]["selectedpoints"] = selection
            return fig
        except TypeError as e:
            print(e)
            return dash.no_update


@app.callback(Output('video-player_b', 'controls'),
              Input('radio-bool-props_b', 'value'))
def update_prop_controls(values):
    return 'controls' in values


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


@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(Output('selected-points-state', 'data'),
              [Input({'type': 'datatable',  'id': ALL}, 'selected_rows'),
               Input('graph-im1_b', 'selectedData'),
               Input('reset-selection_b', 'n_clicks')],
              [State('selected-points-state', 'data'),
               State('graph-im1_b', 'figure')])
def update_selected_rows(selected_rows, selectedData, n_clicks, selected_points, fig):
    default_state = {'angles': [], 'bodyparts': []}
    if selected_points == None: selected_points = default_state
    ctx = dash.callback_context
    # print('616: {}'.format( ctx.triggered[0]['prop_id']))
    if ctx.triggered[0]['prop_id'] == 'reset-selection_b.n_clicks':
        if n_clicks is None:
            return dash.no_update
        else:
            return default_state
    elif ctx.triggered[0]['prop_id'] == 'graph-im1_b.selectedData':
        selection = [point["curveNumber"] for point in selectedData["points"]]
        selection_names = [fig["data"][curve_number]['name'] for curve_number in selection]
        selected_points = update_selected_state(state=selected_points, bodypart_names=selection_names)
        print('state: {}'. format(selected_points))
        return selected_points
    elif ctx.triggered[0]['prop_id'] == '{"id":"table-tab2-main","type":"datatable"}.selected_rows':
        print(selected_rows[0])
        angles = angle_ids_to_angles(selected_rows[0])
        print(angles)
        selected_points = update_selected_state(state=selected_points, angle_names=angles)
        print('state: {}'.format(selected_points))
        return selected_points
    else:
        return default_state


#edw mallon exei provlima

@app.callback(Output({"id":"table-tab2-main","type":"datatable"}, 'selected_rows'),
              Input('graph-im1_b', 'figure.data'),
              State('selected-points-state', 'data'))
def update_selected_row_state(_, selected_points):
    print('here')
    print(selected_points)
    default_state = {'angles': [], 'bodyparts': []}

    if selected_points is None:
        return dash.no_update
    elif selected_points == default_state:
        return []
    else:
        try:
            print('606: '.format(selected_points['angles']))
            return angles_to_ids(selected_points['angles'])
        except Exception as e:
            print(e)
            return dash.no_update


# @app.callback(Output({"id":"table-tab2-main","type":"datatable"}, 'children'),
#               Input('memory-table_b', 'data'),
#               Input('gradient-scheme', 'value'))
# def update_color_figure(df_angles,value):
#     # if not click1 or not click2 or not click3 or not value:
#     #     return dash.no_update
#     #changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     #print(changed_id)
#
#     df_angles = pd.read_json(df_angles)
#     if value == 'Viridis':
#         print(Viridis)
#         colormap = Viridis
#         return render_datatable(df_angles, colormap=colormap)
#     elif value == 'Plasma':
#         colormap = Plasma
#         return render_datatable(df_angles, colormap=colormap)
#     elif value == 'Else':
#         colormap = Else
#         return render_datatable(df_angles, colormap=colormap)
#     else: return dash.no_update


