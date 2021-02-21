import dash_bootstrap_components as dbc
import dash_html_components as html
from components.datatable import render_datatable
from dash.dependencies import Input, Output, State, MATCH
from app import app

def modal(df_angles, frame_no, dtw_alignment=[], index=1, similarity='angle'):
    return html.Div(
        [
            dbc.Button("Table overview", id={'type': 'modal-button-open', 'index': index}),
            dbc.Modal(
                [
                    dbc.ModalHeader("Motion Rug"),
                    dbc.ModalBody(render_datatable(df_angles, frame_no, fullsize='true',similarity= similarity)),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id={'type': 'modal-button-close', 'index': index}, className="ml-auto"
                        )
                    ),
                ],
                id={'type': 'modal', 'index': index},
                centered=True,
                size="xl",
                style={"max-width": "90vw"}
            ),
        ]
    )

@app.callback(
    Output({'type': 'modal', 'index': MATCH}, "is_open"),
    [Input({'type': 'modal-button-open', 'index': MATCH}, "n_clicks"),
     Input({'type': 'modal-button-close', 'index': MATCH}, "n_clicks")],
    [State({'type': 'modal', 'index': MATCH}, "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
