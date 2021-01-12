import dash_table
from dash_table.Format import Format, Scheme
import dash_html_components as html
import dash_bootstrap_components as dbc
from heatmap_table_format import heatmap_table_format, highlight_current_frame, tooltip_angles
from utils import BODYPART_THUMBS_SMALL


def render_datatable(df_angles, frame_no='false', fullsize='false', pagesize=10, dif_table='false', selected_rows=[]):
    if not selected_rows: selected_rows = []

    # Apply table styles
    (styles, legend) = heatmap_table_format(df_angles, selected_rows=selected_rows)
    styles_header = []
    if frame_no != 'false':
        styles_header, extra_styles = highlight_current_frame(frame_no)
        styles.append(extra_styles)

    # Table Overview case
    if fullsize == 'true':
        df_angles.insert(0, 'angles_small', BODYPART_THUMBS_SMALL, True)
        return html.Div([
            html.Div(dbc.ButtonGroup(
                [dbc.Button("Head"), dbc.Button("Torso"), dbc.Button("Arms"), dbc.Button("Legs"), dbc.Button("Feet")],
                size="md",
                className="mr-1",
            )),
            html.Div(legend, style={'float': 'right'}),
            dash_table.DataTable(
                id='table-tab2',
                columns=[
                            {'name': 'angles', 'id': 'angles_small', 'presentation': 'markdown'}] + [
                            {
                                'name': '{}'.format(i[-3:].replace(':', '').replace('e', '')),
                                'id': i,
                                'type': 'numeric',
                                'format': Format(precision=0, scheme=Scheme.fixed),
                            } for i in df_angles.iloc[:, 3:].columns],
                data=df_angles.to_dict('records'),
                fixed_columns={'headers': True, 'data': 1},
                style_data={'font-size': '10px', 'text-align': 'center'},
                style_table={ 'max-width': '100%', 'min-height': '80vh'},
                style_data_conditional=styles,
                tooltip_data=tooltip_angles(type='angles_small'),
                tooltip_delay=0,
                tooltip_duration=None
            ),
        ])
    # Difference table case
    elif dif_table == 'true':
        return html.Div([
            render_frame_header(frame_no),
            html.Div(legend, style={'float': 'right'}),
            dash_table.DataTable(
                id='table-tab2',
                columns=[
                            {'name': 'angles', 'id': 'angles', 'presentation': 'markdown'}] + [
                            {
                                'name': i,
                                'id': i,
                                'type': 'numeric',
                                'format': Format(precision=0, scheme=Scheme.fixed),
                            } for i in df_angles.iloc[:, 2:].columns],
                data=df_angles.to_dict('records'),
                fixed_columns={'headers': True, 'data': 2},
                style_data={'font-size': '18px', 'text-align': 'center',
                            'p': {'margin-block-start': '0px', 'margin-block-end': '0px'}},
                style_table={'overflowX': 'scroll', 'max-width': '100%'},
                style_cell={},
                page_size=pagesize,
                style_data_conditional=styles,
                style_header_conditional=styles_header,
                tooltip_data=tooltip_angles(),
                tooltip_delay=0,
                tooltip_duration=None
            ),
        ])
    # Render default table
    else:
        return html.Div([
            render_frame_header(frame_no),
            html.Div(
                dbc.ButtonGroup(
                [dbc.Button("Groupby", outline=True, color="secondary", disabled=True),
                 dbc.Button("Head", id="head-filter-btn"),
                 dbc.Button("Torso", id="torso-filter-btn"),
                 dbc.Button("Arms", id="arms-filter-btn"),
                 dbc.Button("Legs", id="legs-filter-btn"),
                 dbc.Button("Feet", id="feet-filter-btn")],
                size="md",
                className="mr-1",
            )),
            html.Div(legend, style={'float': 'right'}),
            dash_table.DataTable(
                id={ 'type': 'datatable', 'id': 'table-tab2-main'},
                columns=[
                            {'name': 'angles', 'id': 'angles', 'presentation': 'markdown'}] + [
                            {
                                'name': i,
                                'id': i,
                                'type': 'numeric',
                                'format': Format(precision=2, scheme=Scheme.fixed),
                            } for i in df_angles.iloc[:, 2:].columns],
                data=df_angles.to_dict('records'),
                fixed_columns={'headers': True, 'data': 1},
                style_data={'font-size': '18px', 'text-align': 'center',
                            'p': {'margin-block-start': '0px', 'margin-block-end': '0px'}},
                style_table={'overflowX': 'scroll', 'max-width': '100%'},
                style_cell={},
                row_selectable='multi',
                selected_rows=selected_rows,
                page_size=pagesize,
                style_data_conditional=styles,
                style_header_conditional=styles_header,
                tooltip_data=tooltip_angles(),
                tooltip_delay=0,
                tooltip_duration=None
            ),
        ])


def render_frame_header(frame_no):
    if frame_no != 'false': return html.H4('Current Frame: #{}'.format(frame_no), style={'marginTop': '1%'})
    else: return html.H4()
