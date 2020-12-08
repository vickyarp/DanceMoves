# from textwrap import dedent
#
# import dash_html_components as html
# import dash_core_components as dcc
#
# def modal():
#     return html.Div(
#         children=[
#             html.Div(
#                 html.Div(
#                     className='modal-text',
#                     children=[
#                         dcc.Markdown(dedent('''
#                         # This is the text that will be in the modal
#                         '''))
#                     ]
#                 ),
#             )],
#         id='modal',
#         className='modal',
#         style={"display": "none"},
#     )

import dash_bootstrap_components as dbc
import dash_html_components as html
from datatable import render_datatable

def modal(df_angles, frame_no):
    return html.Div(
        [
            dbc.Button("Table overview", id="open-centered"),
            dbc.Modal(
                [
                    dbc.ModalHeader("Motion Rug (Video #1)"),
                    dbc.ModalBody(render_datatable(df_angles, frame_no, fullsize='true')),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close-centered", className="ml-auto"
                        )
                    ),
                ],
                id="modal-centered",
                centered=True,
                size="xl",
                style={"max-width": "90vw"}
            ),
        ]
    )
