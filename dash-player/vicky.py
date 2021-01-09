import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#import new_visualization
#from page1 import page_1_layout
# from visualization import similarity_layout
from page1_clear import page_1_layout
from visualquery import page_3_layout

from app import app
from clustering_new import get_dendogram
from dataset_info import txt2

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.

#app = dash.Dash(__name__, suppress_callback_exceptions=True)

#server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[])
])



index_page = html.Div([
    html.H1('Visual Analysis of Dance Moves', style={'text-align': 'center'}),
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
    # dcc.Link('Go to Page 1', href='/page-1'),
    # dcc.Link(html.Button(name='back', size="lg", className="mr-1"), href='/page-1'),
    dcc.Link(dbc.Button('Interact with one video', size="lg"), href="/page-1"),
    # html.Br(),
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
    dbc.Button("i", id="open-backdrop",size= 'sm'),
    dbc.Modal(
            [
                dbc.ModalHeader("Video namings"),
                dbc.ModalBody(
                    txt2
                    #"Change the backdrop of this modal with the radio buttons"
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
    html.Div(
    [
        dbc.Button(
            "Hierarchival clustering", id="fade-transition-button", className="mb-3"
        ),
        dbc.Fade(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='graph-dendro',
                        figure=get_dendogram(),
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



    # INSERT IMAGE
    # html.Img(src=app.get_asset_url('Output_Skeleton_ballerina.jpg'),style={'width':328, 'height':328}),
    html.Br(),
    html.P(u"\u00A9"+' Master Project of University of Zurich- Vasiliki Arpatzoglou & Artemis Kardara'
           , style={'text-align': 'center', 'fontSize': 16})

], style={'textAlign': 'center','margin':'auto','width': "50%"})


@app.callback(
    Output("fade-transition", "is_in"),
    [Input("fade-transition-button", "n_clicks")],
    [State("fade-transition", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in




# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout

    # elif pathname == '/page-2':
    #     return similarity_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


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
