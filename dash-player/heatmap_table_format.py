import dash_html_components as html
from utils import BODYPART_INDEX
import plotly.express as px
viridis = [
 # '#440154',
 # '#482878',
 '#3e4989',
 # '#31688e',
 # '#26828e',
 '#1f9e89',
 '#35b779',
 # '#6ece58',
 # '#b5de2b',
 '#fde725'
]
colormap = [
    '#f0f9e8',
    '#bae4bc',
    '#7bccc4',
    '#2b8cbe',
]

def heatmap_table_format(df, n_bins=4, columns='all', selected_rows=[]):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        # backgroundColor = colorlover.scales[str(n_bins)]['seq']['YlGnBu'][i - 1]
        backgroundColor = colormap[i-1]
        color = 'black' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color,
            })
        for row in selected_rows:
            styles.append({
                'if': {
                    # 'row_index': row,
                    'filter_query': '{{id}} contains {}'.format(str(row)),
                    'column_id': 'angles'
                },
                'backgroundColor': 'black',
                'color': 'black'
            })

        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )
    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

def highlight_current_frame(frame_no):
    header_styles = []
<<<<<<< HEAD
    header_styles.append({ 'if': { 'column_id': 'Frame:{}'.format(frame_no), 'header_index': 0 }, 'color': 'white', 'backgroundColor': 'black' },)
    return header_styles
=======
    header_styles.append({
        'if': { 'column_id': 'Frame:{}'.format(frame_no), 'header_index': 0 },
        'color': 'white',
        'backgroundColor': 'black',
        'border': '3px black solid'
    })
    styles = {'if': {'column_id': 'Frame:{}'.format(frame_no), }, 'border-right': '3px black solid', 'border-left': '3px black solid'}
    return header_styles, styles

>>>>>>> 2ce7f19... angle highlighting first attempt
def tooltip_angles(bodyparts=BODYPART_INDEX, type='angles'):
    tooltip = []
    for key, value in BODYPART_INDEX.items():
        tooltip.append({type: value})
    return tooltip
# tooltip_angles =[
#         {
#             'angles': 'nose_to_neck_to_left_shoulder',
#         },
#         {
#             'angles': 'nose_to_neck_to_right_shoulder',
#         },
#         {
#             'angles': 'left_shoulder_to_right_shoulder',
#         },
#         {
#             'angles': 'left_shoulder_to_left_upper_arm',
#         },
#         {
#             'angles': 'left_lower_arm_to_left_upper_arm',
#         },
#         {
#             'angles': 'right_upper_arm_to_right_shoulder',
#         },
#         {
#             'angles': 'right_upper_arm_to_right_lower_arm',
#         },
#         {
#             'angles': 'left_eye_to_nose_to_left_ear_to_eye',
#         },
#         {
#             'angles': 'left_eye_to_nose_to_neck',
#         },
#         {
#             'angles': 'nose_to_neck_to_right_eye_to_nose',
#         },
#         {
#             'angles': 'left_eye_to_nose_to_right_ear_to_eye',
#         },
#         {
#             'angles': 'right_eye_to_nose_to_right_ear_to_eye',
#         },
#         {
#             'angles': 'right_hip_to_right_upper_leg',
#         },
#         {
#             'angles': 'right_upper_leg_to_right_lower_leg',
#         },
#         {
#             'angles': 'left_hip_to_left_upper_leg',
#         },
#         {
#             'angles': 'left_upper_leg_to_left_lower_leg',
#         },
#         {
#             'angles': 'left_lower_leg_left_ankle_to_heel',
#         },
#         {
#             'angles': 'right_lower_leg_to_right_ankle_to_heel',
#         },
#         {
#             'angles': 'right_foot_to_right_toes',
#         },
#         {
#             'angles': 'right_foot_to_right_lower_leg',
#         },
#         {
#             'angles': 'right_foot_to_right_ankle_to_heel',
#         },
#         {
#             'angles': 'left_foot_to_left_lower_leg',
#         },
#         {
#             'angles': 'left_foot_to_left_ankle_to_heel',
#         },
#         {
#             'angles': 'left_foot_to_left_toes',
#         },
#         {
#             'angles': 'torso_to_right_shoulder',
#         },
#         {
#             'angles': 'torso_to_left_shoulder',
#         },
#         {
#             'angles': 'torso_to_nose_to_neck',
#         },
#         {
#             'angles': 'torso_to_right_hip',
#         },
#         {
#             'angles': 'torso_to_left_hip',
#         },
#     ]
#
# tooltip_angles_small =[
#         {
#             'angles_small': 'nose_to_neck_to_left_shoulder',
#         },
#         {
#             'angles_small': 'nose_to_neck_to_right_shoulder',
#         },
#         {
#             'angles_small': 'left_shoulder_to_right_shoulder',
#         },
#         {
#             'angles_small': 'left_shoulder_to_left_upper_arm',
#         },
#         {
#             'angles_small': 'left_lower_arm_to_left_upper_arm',
#         },
#         {
#             'angles_small': 'right_upper_arm_to_right_shoulder',
#         },
#         {
#             'angles_small': 'right_upper_arm_to_right_lower_arm',
#         },
#         {
#             'angles_small': 'left_eye_to_nose_to_left_ear_to_eye',
#         },
#         {
#             'angles_small': 'left_eye_to_nose_to_neck',
#         },
#         {
#             'angles_small': 'nose_to_neck_to_right_eye_to_nose',
#         },
#         {
#             'angles_small': 'left_eye_to_nose_to_right_ear_to_eye',
#         },
#         {
#             'angles_small': 'right_eye_to_nose_to_right_ear_to_eye',
#         },
#         {
#             'angles_small': 'right_hip_to_right_upper_leg',
#         },
#         {
#             'angles_small': 'right_upper_leg_to_right_lower_leg',
#         },
#         {
#             'angles_small': 'left_hip_to_left_upper_leg',
#         },
#         {
#             'angles_small': 'left_upper_leg_to_left_lower_leg',
#         },
#         {
#             'angles_small': 'left_lower_leg_left_ankle_to_heel',
#         },
#         {
#             'angles_small': 'right_lower_leg_to_right_ankle_to_heel',
#         },
#         {
#             'angles_small': 'right_foot_to_right_toes',
#         },
#         {
#             'angles_small': 'right_foot_to_right_lower_leg',
#         },
#         {
#             'angles_small': 'right_foot_to_right_ankle_to_heel',
#         },
#         {
#             'angles_small': 'left_foot_to_left_lower_leg',
#         },
#         {
#             'angles_small': 'left_foot_to_left_ankle_to_heel',
#         },
#         {
#             'angles_small': 'left_foot_to_left_toes',
#         },
#         {
#             'angles_small': 'torso_to_right_shoulder',
#         },
#         {
#             'angles_small': 'torso_to_left_shoulder',
#         },
#         {
#             'angles_small': 'torso_to_nose_to_neck',
#         },
#         {
#             'angles_small': 'torso_to_right_hip',
#         },
#         {
#             'angles_small': 'torso_to_left_hip',
#         },
#     ]
