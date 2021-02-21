import os
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from settings import POSE_PATH
from components.datatable import render_datatable
from metrics.overall_video_similarity import pose_query
from app import app
from dash.dependencies import Input, Output
from settings import BODYPART_THUMBS, POSES_DICT


def visual_query_layout():
    df_angles_dif = pose_query()
    df_angles_dif.insert(0, 'angles', BODYPART_THUMBS, True)
    return html.Div(
        style={
            'width': '80%',
            'float': 'left',
            'margin': '1% 0% 2% 0%'
        },
        children = [
            dbc.Col(
                id='col-queries',
                style={
                    'width': '15%',
                    'float': 'left',
                    'margin': 0,
                    'max-height': '80vh',
                },
                children=[
                    pose_card('LU_S_big_frame_52.png', key='qsearch-1', title= 'First Arabesque'),
                    pose_card('TOS_F_frame_38.png', key='qsearch-2', title='Demi-plié (in 5th position)'),
                    pose_card('CU_R_NA_frame_6.png', key='qsearch-3', title= 'Relevé (in 3rd position)')],

            ),
            dbc.Col(
                id='cl2',
                style={
                    'width': '85%',
                    'float': 'left',
                    'margin': 0
                },
                children=[dbc.Card(id='dif-table', children=[])]),
    ])


def render_card_body():
    return dbc.CardBody(
        [
            html.H5("Arabesque", className="card-title"),
            html.P("This card has some text content, but not much else"),
            dbc.Button("Select", color="primary"),
        ]
    )

def pose_card(img, key, title="Pose"):
    card = dbc.Card(
        [
            dbc.CardImg(src=os.path.join(POSE_PATH, img), top=True),
            dbc.CardBody(
                [
                    html.H4(title, className="card-title"),
                    dbc.Button("Search pose", id=key, n_clicks=0, color="primary"),
                ]
            ),
        ],
        style={"width": "14rem"},
    )
    return card


### Search Query callbacks

@app.callback(Output('dif-table', 'children'),
              [Input('memory-video1_b', 'value'),
               Input('memory-frame_b', 'data'),
               Input('qsearch-1', 'n_clicks'),
               Input('qsearch-2', 'n_clicks'),
               Input('qsearch-3', 'n_clicks')],
              )
def render_dif_table(value, frame_no, click1, click2, click3):
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
    return render_datatable(df_angles_dif, pagesize=13, frame_no=frame_no, dif_table='true', similarity='velocity')
