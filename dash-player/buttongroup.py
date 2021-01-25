import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
from app import app

GROUPBY_SELECTION = {
    0 : {'angles':
            [
                'left_eye_to_nose_to_left_ear_to_eye',
                'left_eye_to_nose_to_neck',
                'nose_to_neck_to_right_eye_to_nose',
                'left_eye_to_nose_to_right_ear_to_eye',
                'right_eye_to_nose_to_right_ear_to_eye',
            ],'bodyparts': []

        },
    1 : {'angles':
             [
                'torso_to_right_shoulder',
                'torso_to_left_shoulder',
                'torso_to_nose_to_neck',
                'torso_to_right_hip',
                'torso_to_left_hip',

             ], 'bodyparts': []},
    2: {'angles':
        [
            'nose_to_neck_to_left_shoulder',
            'nose_to_neck_to_right_shoulder',
            'left_shoulder_to_right_shoulder',
            'left_shoulder_to_left_upper_arm',
            'left_lower_arm_to_left_upper_arm',
            'right_upper_arm_to_right_shoulder',
            'right_upper_arm_to_right_lower_arm',

        ], 'bodyparts': []},
    3: {'angles':
        [
            'right_hip_to_right_upper_leg',
            'right_upper_leg_to_right_lower_leg',
            'left_hip_to_left_upper_leg',
            'left_upper_leg_to_left_lower_leg',
            'left_lower_leg_left_ankle_to_heel',
            'right_lower_leg_to_right_ankle_to_heel',
        ], 'bodyparts': []},
    4: {'angles':
        [
            'right_foot_to_right_toes',
            'right_foot_to_right_lower_leg',
            'right_foot_to_right_ankle_to_heel',
            'left_foot_to_left_lower_leg',
            'left_foot_to_left_ankle_to_heel',
            'left_foot_to_left_toes',
        ], 'bodyparts': []},
}

def buttongroup():
    return html.Div(
        dbc.ButtonGroup(
            [dbc.Button("Groupby", outline=True, color="secondary", disabled=True),
             dbc.Button("Head", id={'type': 'group-by-button', 'index':0}, n_clicks_timestamp=0),#id="head-filter-btn"),
             dbc.Button("Torso", id={'type': 'group-by-button', 'index':1}, n_clicks_timestamp=0),
             dbc.Button("Arms", id={'type': 'group-by-button', 'index':2}, n_clicks_timestamp=0),
             dbc.Button("Legs", id={'type': 'group-by-button', 'index':3}, n_clicks_timestamp=0),
             dbc.Button("Feet", id={'type': 'group-by-button', 'index':4}, n_clicks_timestamp=0)],
            size="md",
            className="mr-1",
        ))

