import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from layouts.compare_videos import similarity_layout
from layouts.analyze_video import page_1_layout
from layouts.visual_query import page_3_layout

from app import app
from metrics.clustering import get_dendogram_angle, get_dendogram_velocity
from layouts.dataset_info import txt2


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])

index_page = html.Div([
    html.H1('Visual Analysis of Dance Moves', style={'text-align': 'center', 'padding-top': '3rem', 'margin-bottom': '3rem'}),
    html.Img(src=app.get_asset_url('logo.png'), style={'width':328}),
    html.P('The goal of this project is to build a tool for the visual analysis of dance moves.', style={'text-align': 'center','fontSize': 26}),
    html.Hr(className="my-2"),
    html.Br(),
    html.P('In general, the term "pose" is used to describe stationary dance positions. '
            'In our case, is used to describe a sequence of movements. These dance movements of a single dancer may '
            'be further detailed into different body, head, arm, hand, leg, and foot positions. '
            'Ballet and contemporary dance is our main interest of dance types, with possibility of expansion.'
            , style={'text-align': 'center','fontSize': 26}),
    html.Br(),

    html.Div([
        html.P('Go to the analysis'),
    ], style={'marginBottom': 50, 'marginTop': 25, 'fontSize': 26}),
    dcc.Link(dbc.Button('Interact with one video', size="lg"), href="/page-1"),
    dcc.Link(dbc.Button('Interact with two videos and find similarity', size="lg"), href="/page-2"),
    dcc.Link(dbc.Button('Interact with visual query', size="lg"), href="/page-3"),

    html.Br(),
    html.Br(),
    html.P(' The dataset we are using is called "Dataset - MultiTime Laboratory H-Dance Database". '
           'It contains ballet poses with variations of each pose:'
           , style={'text-align': 'center', 'fontSize': 26}),
    html.Br(),
    html.Li('faster vs. slower movement',style={'fontSize': 26}),
    html.Li('right vs. left movement ',style={'fontSize': 26}),
    html.Li('front vs. backwards movement ',style={'fontSize': 26}),
    html.Li('with arm vs. without arm movement ',style={'fontSize': 26}),
    html.Li('big vs small movement',style={'fontSize': 26}),
    html.Br(),
    html.A(' Dataset', href='https://figshare.com/articles/dataset/H_Dance_Database/1453169', target='_blank' ,style={'fontSize': 26}),
    html.Br(),
    dbc.Button("Dataset Information ", id="open-backdrop",size= 'lg',style={'font-weight': 'bold' }),
    dbc.Modal(
            [
                dbc.ModalHeader("Video namings"),
                dbc.ModalBody(
                    txt2
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close-backdrop", className="ml-auto"
                    )
                ),
            ],
            id="modal-backdrop",
            scrollable=True,
            size="xl",
        ),
    html.Br(),
    html.Br(),
    html.H4('Hierarchical Clustering:'),
    html.Div(
    [
        dbc.Button(
            "Angle Similarity", id={"type": "fade-transition-button", "index": 1}, className="mb-3", style={'margin-right': '10px'}, n_clicks_timestamp=0,
        ),
        dbc.Button(
            "Velocity Similarity", id={"type": "fade-transition-button", "index": 2}, className="mb-3", style={'margin-right': '10px'}, n_clicks_timestamp=0
        ),
        dbc.Fade(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id="graph-dendro",
                        style={"display": "block", "margin-left": "auto", "margin-right": "auto"},
                    )
                )
            ),
            id="fade-transition",
            is_in=False,
            appear=False,
            style={"transition": "opacity 100ms ease"},
        ),
    ]
    ),

    html.Br(),
    html.P(u"\u00A9"+' Master Project of University of Zurich- Vasiliki Arpatzoglou & Artemis Kardara'
           , style={'text-align': 'center', 'fontSize': 16})

], style={'textAlign': 'center','margin':'auto','width': "50%",
            'background-image': 'url("/assets/background2.png")'})

@app.callback(
    [Output("fade-transition", "is_in"),
     Output("graph-dendro", "figure")],
    Input({"type": "fade-transition-button", "index":ALL}, "n_clicks_timestamp"),
    State("fade-transition", "is_in"))
def toggle_fade(n1, is_in):
    print('MODAL')
    try:
        if not n1:
            return False, dash.no_update
        elif n1[0] > n1[1]:
            fig = get_dendogram_angle()
            return not is_in, fig
        elif n1[0] < n1[1]:
            fig = get_dendogram_velocity()
            return not is_in, fig
    except Exception as e:
        print(e)
    return dash.no_update, dash.no_update

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout

    elif pathname == '/page-2':
         return similarity_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_page


#for modal
@app.callback(
    Output("modal-backdrop", "backdrop"), [Input("backdrop-selector", "value")]
)
def select_backdrop(backdrop):
    return backdrop


@app.callback(
    Output("modal-backdrop", "is_open"),
    [Input("open-backdrop", "n_clicks"), Input("close-backdrop", "n_clicks")],
    [State("modal-backdrop", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
