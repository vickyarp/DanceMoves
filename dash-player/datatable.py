import dash_table
from dash_table.Format import Format, Scheme
import dash_html_components as html
from heatmap_table_format import heatmap_table_format, highlight_current_frame, tooltip_angles, tooltip_angles_small
from utils import BODYPART_THUMBS_SMALL


def render_datatable(df_angles, frame_no, fullsize='false'):
    (styles, legend) = heatmap_table_format(df_angles)
    styles_header = highlight_current_frame(frame_no)
    if fullsize == 'true':
        df_angles.insert(0, 'angles_small', BODYPART_THUMBS_SMALL, True)
        return html.Div([
            html.Div(legend, style={'float': 'right'}),
            dash_table.DataTable(
                id='table-tab2',
                columns=[
                            {'name': 'angles', 'id': 'angles_small', 'presentation': 'markdown'}] + [
                            {
                                'name': '{}'.format(i[-3:-1]),
                                'id': i,
                                'type': 'numeric',
                                'format': Format(precision=0, scheme=Scheme.fixed),
                            } for i in df_angles.iloc[:, 3:].columns],
                data=df_angles.to_dict('records'),
                fixed_columns={'headers': True, 'data': 1},
                style_data={'font-size': '10px', 'text-align': 'center'},
                style_table={ 'max-width': '100%', 'min-height': '80vh'},
                style_data_conditional=styles,
                tooltip_data=tooltip_angles_small,
                tooltip_delay=0,
                tooltip_duration=None
            ),
        ])
    else:
        return  html.Div([
            html.H4('Frame #{}'.format(frame_no)),
            html.Div(legend, style={'float': 'right'}),
            dash_table.DataTable(
                id='table-tab2',
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
                page_size=10,
                style_data_conditional=styles,
                style_header_conditional=styles_header,
                tooltip_data=tooltip_angles,
                tooltip_delay=0,
                tooltip_duration=None
            ),
        ])
