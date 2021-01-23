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
    dcc.Location(id='url', refresh=False, pathname='/page-1'),
    html.H1('Interact with one video', style={'text-align': 'center'}),
    html.Br(),
    html.Div(
        [
            dcc.Link(dbc.Button('Go back to home page', size="lg"), href="/"),
            dcc.Link(dbc.Button('Interact with two videos and find similarity', size="lg"), href="/page-2"),
            dcc.Link(dbc.Button('Interact with visual query', size="lg"), href="/page-3"),
        ],
        style={ 'display': 'flex', 'justify-content': 'center'}),

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
                    figure=go.Figure(),
                    style={'height': '50vh'}
                ),
                html.Div(
                    children=[dbc.Button("Update", id="update-selection_b", style={'margin': '5px'}),
                              dbc.Button("Reset", id="reset-selection_b", style={'margin': '5px'})],
                    style={'display': 'flex', 'justify-content': 'center'}
                ),
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
    df_angles.insert(1, 'id', [i for i in range(29)], True)
    keypoints1 = get_keypoints(video_selected1)
    data = []
    for frame in keypoints1:
        df = create_coordinate_df(frame)
        data.append(df.to_json())
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
              [Input('video-player_b', 'currentTime'),
               Input('range-slider_b', 'value')],
              [State('video-player_b', 'duration'),
               State('video-player_b', 'playing')])
def update_position(currentTime, value, duration, playing):
    start = list(value)[0]
    end = list(value)[1]
    try:
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] == 'range-slider_b.value':
            if not playing and currentTime > 1:
                return start
            elif not playing:
                percentage = (start / duration)
                return percentage
            else:
                dash.no_update
        elif ctx.triggered[0]['prop_id'] == 'video-player_b.currentTime':
            if currentTime and currentTime >= end:
                if currentTime > 1:
                    return start
                else:
                    percentage = (start / duration)
                    return percentage
            else:
                return dash.no_update
        else:
            return dash.no_update
    except Exception as e:
        print(e)
        return dash.no_update


@app.callback(Output('tabs-content_b', 'children'),
              [Input('table-tabs_b', 'value'),
               Input('memory-output1_b', 'data'),
               Input('memory-table_b', 'data'),
               Input('video-player_b', 'playing'),
               Input('selected-row-state', 'data'),
               Input('gradient-scheme', 'value'),
               Input('memory-frame_b', 'data')],
               [State('video-player_b', 'currentTime')])
def render_content(tab, dft, df_angles, playing, selected_rows, gradient_scheme, frame_no, currentTime):
    try:
        if tab == 'tab-1':
            df = dft[frame_no]
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
                        'backgroundColor': colormaps[gradient_scheme][2],
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
            return render_datatable(df_angles, frame_no, selected_rows=selected_rows, colormap=colormaps[gradient_scheme]), modal(df_angles, frame_no)
    except:
        return dash.no_update


@app.callback(Output('graph-im1_b', 'figure'),
              [Input('video-player_b', 'playing'),
               Input('memory-frame_b', 'data'),
               Input('reset-selection_b', 'n_clicks'),
               Input('selected-points-state_b', 'data')],
              [State('memory-output1_b', 'data'),
               State('memory-video1_b', 'value'),
               State('graph-im1_b', 'figure')])
def update_figure(playing, frame_no, n_clicks, selected_points, video_frames, video1, fig):
    try:
        ctx = dash.callback_context
        if ctx.triggered[0]['prop_id'] in ['video-player_b.playing', 'memory-frame_b.data']:
            try:
                if not playing and frame_no:
                    df = pd.read_json(video_frames[frame_no])
                    return render_stick_figure(df, video1)
                else: return dash.no_update
            except:
                return dash.no_update
        # elif ctx.triggered[0]['prop_id'] == 'reset-selection_b.n_clicks':
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

                if ctx.triggered[0]['prop_id'] == 'selected-points-state_b.data':
                    for bodypart in selected_points['bodyparts']:
                        curve = next(filter(lambda x: x['name'] == bodypart,  fig["data"]))
                        curve_number = fig["data"].index(curve)
                        fig["data"][curve_number]["line"]["color"] = COLORS[curve_number]
                        fig["data"][curve_number]["line"]["width"] = 5
                        fig["data"][curve_number]["opacity"] = 1
                return fig
            except TypeError as e:
                print(e)
                return dash.no_update
    except:
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


# @app.callback(
#     Output("modal-centered", "is_open"),
#     [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
#     [State("modal-centered", "is_open")])
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open


@app.callback(Output('selected-points-state_b', 'data'),
              [Input({'type': 'datatable',  'id': ALL}, 'derived_virtual_selected_row_ids'),
               Input('graph-im1_b', 'selectedData'),
               Input('reset-selection_b', 'n_clicks')],
              [State('selected-points-state_b', 'data'),
               State('graph-im1_b', 'figure')])
def update_selected_rows(selected_rows, selectedData, n_clicks, selected_points, fig):
    try:
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
            print('selected data to state: {}'.format(selected_points))
            return selected_points
        elif ctx.triggered[0]['prop_id'] == '{"id":"table-tab2-main","type":"datatable"}.derived_virtual_selected_row_ids':
            angles = angle_ids_to_angles(selected_rows[0])
            print(angles)
            selected_points = update_selected_state(state=selected_points, angle_names=angles)
            print('derived_virtual_selected_row_ids: {} -> selected_points: {}'.format(selected_rows, selected_points))
            return selected_points
        else:
            return default_state
    except:
        return dash.no_update


@app.callback([Output({"id":"table-tab2-main","type":"datatable"}, 'selected_rows'),
               Output({"id":"table-tab2-main","type":"datatable"}, 'data')],
              [Input('selected-points-state_b', 'data'),
               Input({'id': 'table-tab2-main', 'type': 'datatable'}, 'sort_by'),
               Input({'id': 'table-tab2-main', 'type': 'datatable'}, 'selected_row_ids')],
              [State('selected-points-state_b', 'data'),
              State({"id":"table-tab2-main","type":"datatable"}, 'derived_virtual_selected_row_ids'),
               State({'id':'table-tab2-main','type':'datatable'}, 'derived_virtual_selected_rows'),
               State({'id': 'table-tab2-main', 'type': 'datatable'}, 'data')])
def update_selected_row_state(_, sort_by, selected_row_ids, selected_points_state, derived_virtual_selected_row_ids, derived_virtual_selected_rows, data):
    try:
        default_state = {'angles': [], 'bodyparts': []}
        ctx = dash.callback_context
        sort_by_trigger = '{"id":"table-tab2-main","type":"datatable"}.sort_by'
        selected_id_trigger = '{"id":"table-tab2-main","type":"datatable"}.selected_row_ids'

        if ctx.triggered[0]['prop_id'] == 'selected-points-state_b.data':
            if selected_points_state is None:
                return dash.no_update, dash.no_update
            elif selected_points_state == default_state:
                return [], dash.no_update
            else:
                print('490: {}'.format(selected_points_state['angles']))
                selected = angles_to_ids(selected_points_state['angles'])
                print('-> {}'.format(selected))
                for i in range(len(selected)):
                    row = selected[i]
                    index = next((j for j, item in enumerate(data) if item['id'] == row), -1)
                    data.insert(i, data.pop(index))
                return [i for i in range(len(selected))], data

        elif ctx.triggered[0]['prop_id'] == sort_by_trigger or ctx.triggered[0]['prop_id'] == selected_id_trigger:
                print('(665) selected_row_ids: {}'.format(selected_row_ids))
                selected_row_ids.sort()
                for i in range(len(selected_row_ids)):
                    row = selected_row_ids[i]
                    index = next((j for j, item in enumerate(data) if item['id'] == row), -1)
                    data.insert(i, data.pop(index))
                derived_virtual_selected_rows = [i for i in range(len(selected_row_ids))]
                return derived_virtual_selected_rows, data
    except Exception as e:
        print(e)
        return dash.no_update, dash.no_update
    return dash.no_update, dash.no_update


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


