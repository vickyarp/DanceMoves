import dash
import dash_player
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from utils import DATASET_VIDEOS,BODYPART_THUMBS
from dash.dependencies import Input, Output, State
from keypoint_frames import create_df
from keypoint_frames import get_keypoints

from new_visualization import get_coordinates, create_coordinate_df
from overall_video_similarity import create_angles, overall_similarity
from app import app

DURATION = 4.105


page_1_layout = html.Div([
    html.H1('Interact with one video', style={'text-align': 'center'}),
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
            dcc.Store(id='memory-output3'),
            dcc.Store(id='memory-output4'),
            dcc.Store(id='memory-table5'),
            dcc.Store(id='current-time3'),
            dcc.Store(id='current-time4'),
            dcc.Store(id='memory-frame3'),

            # dcc.Input(
            #     id='input-url',
            #     value='/assets/TB_F_FB.mp4'
            # ),
            # html.Button('Change video', id='button-update-url'),
            html.P("Choose Main Video:"),
            dcc.Dropdown(
                id='memory-video3',
                options=[{'value': x, 'label': x} for x in DATASET_VIDEOS],
                value='BA_R_WA'
            ),

            dash_player.DashPlayer(
                id='video-player3',
                #url='/assets/TB_F_FB.mp4',#t=npt:2.3,2.9',
                currentTime= 0,
                controls=True,
                intervalCurrentTime=40,
                loop=True,
                width='100%'
            ),
            html.Div(
                id='div-current-time3',
                style={'margin': '10px 0px'}
            ),

            html.Div(
                id='div-method-output3',
                style={'margin': '10px 0px'}
            ),

            dcc.Checklist(
                id='radio-bool-props3',
                options=[{'label': val.capitalize(), 'value': val} for val in [
                    'playing',
                    'loop',
                    'controls',
                    'muted'
                ]],
                value=['loop', 'muted']
            ),

            html.P("Playback Range: {}", id='output-container-range-slider3'),
            dcc.RangeSlider(
                id='range-slider3',
                min=0,
                max=DURATION,
                step=0.001,
                value=[0, 3],
                updatemode='drag',
                # marks={i: "%g" %i for i in np.arange(0, 10, 0.1)},
            ),


            html.P("Playback Rate:", style={'margin-top': '20px'}),
            dcc.Slider(
                id='slider-playback-rate3',
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
                id='memory-video4',
                options=[{'value': x, 'label': x} for x in DATASET_VIDEOS],
                value='BA_R_NA'
            ),
            dash_player.DashPlayer(
                id='video-player4',
                #url='/assets/TB_F_FB.mp4',#t=npt:2.3,2.9',
                currentTime= 0,
                intervalCurrentTime = 100,
                loop=True,
                controls=True,
                width='100%'
            ),
            html.Div(
                id='div-current-time4',
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
        ]),
    ]),
])



@app.callback([Output('video-player3', 'playing'),
               Output('video-player4', 'playing')],
              [Input('radio-bool-props3', 'value')])
def update_prop_playing(values):
    return 'playing' in values, 'playing' in values


@app.callback([Output('video-player3', 'loop'),
               Output('video-player4', 'loop')],
              [Input('radio-bool-props3', 'value')])
def update_prop_loop(values):
    return 'loop' in values, 'loop' in values


@app.callback(
    [Output('output-container-range-slider3', 'children'),
     Output('range-slider3', 'max')],
    [Input('range-slider3', 'value'),
     Input('video-player3', 'duration')])
def update_output(value, duration):
    if duration:
        return 'Playback range: "{}"'.format(value), duration
    else:
        return 'Playback range: "{}"'.format(value), dash.no_update

@app.callback(Output('memory-frame3', 'data'),
              Input('video-player3', 'currentTime'))
def update_current_frame(currentTime):
    try:
        frame_no = int(np.round(currentTime / .04))
        return frame_no
    except:
        return 0

@app.callback([Output('video-player3', 'seekTo'),
               Output('video-player4', 'seekTo')],
              [Input('video-player3', 'currentTime'),
              ],# Input('range-slider', 'value')],
             [State('range-slider3', 'value'),
               State('video-player4', 'currentTime'),
              State('video-player3', 'duration')])
def update_position(currentTime, value, currentTime2, duration):
    start = list(value)[0]
    end = list(value)[1]
    if currentTime and currentTime >= end:
        if currentTime > 1:
            return start, start
        else:
            percentage = (start / duration)
            return percentage, percentage
            # return 0, 0
    else:
        return dash.no_update, dash.no_update

