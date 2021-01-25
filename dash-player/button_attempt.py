# from app import app
# import dash_core_components as dcc
# import dash_bootstrap_components as dbc
# import dash_html_components as html
#
#
# def make_button(placement):
#     return dbc.Button(
#         f"Tooltip on {placement}",
#         id=f"tooltip-target-{placement}",
#         className="mx-2",
#     )
#
#
# def make_tab(placement):
#     return dcc.Tab(
#         f"Tooltip on {placement}",
#         id=f"tooltip-target-{placement}",
#         className="mx-2",
#     )
#
#
# def make_tooltip(placement):
#     return dbc.Tooltip(
#         f"Tooltip on {placement}",
#         target=f"tooltip-target-{placement}",
#         placement=placement,
#     )
#
#
# app.layout = html.Div(
#     [make_tab("bottom")]
#     + [make_tooltip("bottom")]
# )
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)


import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


tabs_data = [
    {
        "label": "Tab 1",
        "id": "tab-1",
        "tooltip-text": "This is tab 1",
        "content": "This is the content of tab 1",
    },
    {
        "label": "Tab 2",
        "id": "tab-2",
        "tooltip-text": "This tab is tab 2",
        "content": "Here's some stuff under tab 2",
    },
    {
        "label": "Other",
        "id": "tab-other",
        "tooltip-text": "This is a different tab",
        "content": "Blah blah blah",
    },
]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

tabs = dcc.Tabs(
    [
        # dcc.Tab(
        #     html.Div(tab["content"], className="p-2"),
        #     label=tab["label"],
        #     id=tab["id"],
        # )
        # for tab in tabs_data

    dcc.Tab(label='Angle Similarity', id='tab-2'),
    dcc.Tab(label='Velocity Similarity', value='tab-1')
    ]
)

# tooltips = [
#     dbc.Tooltip(tab["tooltip-text"], target=tab["id"]) for tab in tabs_data
# ]

tooltips = [
    dbc.Tooltip("tooltip-text", target='tab-2')
]


app.layout = dbc.Container([tabs] + tooltips, className="p-3")

if __name__ == "__main__":
    app.run_server(debug=True)