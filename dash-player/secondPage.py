import os

import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_reusable_components as drc

from utils import POSE_PATH, BODYPART_THUMBS
from datatable import render_datatable
from overall_video_similarity import pose_query


def secondPage():
    df_angles_dif = pose_query()
    df_angles_dif.insert(0, 'angles', BODYPART_THUMBS, True)
    # df_angles_dif = df_angles_dif.to_json()
    return html.Div([
        #html.H2('Variation of Poses in Video'),
        dbc.Row(id= 'row', children=[
            dbc.Col(
                id='col-queries',
                children=[
                    pose_card('TB_S_FB_frame43.png', key='qsearch-1'),
                    pose_card('PC_F_frame_72.png', key='qsearch-2'),
                    pose_card('SYN_K_frame22.png', key='qsearch-3')],
                width=2
            ),
            dbc.Col(id='cl2', children=[dbc.Card(id='dif-table', children=[])], width=10),
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

