import os
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_reusable_components as drc
from utils import POSE_PATH, BODYPART_THUMBS
from datatable import render_datatable
from overall_video_similarity import pose_query
from app import app
from dash.dependencies import Input, Output
from utils import COLORS, PAIRS_RENDER, DATASET_VIDEOS, BODYPART_THUMBS, POSES_DICT


def secondPage():
    df_angles_dif = pose_query()
    df_angles_dif.insert(0, 'angles', BODYPART_THUMBS, True)
    # df_angles_dif = df_angles_dif.to_json()
    return html.Div([
        #html.H2('Variation of Poses in Video'),
        dbc.Row(id='row', children=[
            dbc.Col(
                id='col-queries',
                children=[
                    pose_card('TB_S_FB_frame43.png', key='qsearch-1'),
                    pose_card('PC_F_frame_72.png', key='qsearch-2'),
                    pose_card('SYN_K_frame22.png', key='qsearch-3')],
            ),
            dbc.Col(id='cl2', children=[dbc.Card(id='dif-table', children=[])]),

        ]),
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
                    # html.P(
                    #     "Some quick example text to build on the card title and "
                    #     "make up the bulk of the card's content.",
                    #     className="card-text",
                    # ),
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
