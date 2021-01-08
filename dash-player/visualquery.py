import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from modal import modal

from app import app
from overall_video_similarity import pose_query
from utils import  BODYPART_THUMBS, POSES_DICT
from datatable import render_datatable
from secondPage import secondPage


page_3_layout = html.Div([
    html.H1('Visual query', style={'text-align': 'center'}),
    html.Br(),
    dcc.Link(dbc.Button('Go back to home page', size="lg"), href="/"),
    #dcc.Link('Go back to home', href='/'),
    secondPage(),
    html.Br(),
    html.P(u"\u00A9" + ' Master Project of University of Zurich- Vasiliki Arpatzoglou & Artemis Kardara'
           , style={'text-align': 'center', 'fontSize': 16})
])

