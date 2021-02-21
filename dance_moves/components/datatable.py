import dash_table
import dash
from dash_table.Format import Format, Scheme
import dash_html_components as html
from components.heatmap_table_format import heatmap_table_format, highlight_current_frame, highlight_aligned_frame, tooltip_angles
from settings import BODYPART_THUMBS_SMALL



def render_datatable(df_angles, frame_no='false', aligned_frame_no=[], fullsize='false', pagesize=10, dif_table='false', mode='', selected_rows=[], colormap='Else', similarity='angle'):
    try:
        if not selected_rows: selected_rows = []

        # Apply table styles
        if similarity == 'angle':
            (styles, legend) = heatmap_table_format(df_angles, selected_rows=selected_rows, colormap = colormap)
            styles_header = []
        else:
            (styles, legend) = heatmap_table_format(df_angles, selected_rows=selected_rows, colormap=colormap, similarity ='velocity')
            styles_header = []
        if frame_no != 'false':
            styles_header, extra_styles = highlight_current_frame(frame_no)
            styles.append(extra_styles)
        if aligned_frame_no:
            extra_styles_header, extra_styles = highlight_aligned_frame(aligned_frame_no)
            styles_header.append(extra_styles_header)
            styles = styles + extra_styles

        # Table Overview case
        if fullsize == 'true':
            df_angles.insert(0, 'angles_small', BODYPART_THUMBS_SMALL, True)
            return html.Div([
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
                    style_data={'font-size': '10px', 'text-align': 'center','fontWeight': 'bold'},
                    style_table={'max-width': '100%', 'min-height': '80vh'},
                    style_data_conditional=styles,
                    tooltip_data=tooltip_angles(type='angles_small'),
                    tooltip_delay=0,
                    tooltip_duration=None,
                    export_format='csv',
                    export_headers='names',
                ),
            ])
        # Pixel table case
        if mode == 'pixel':
            # df_angles.insert(0, 'angles_tiny', BODYPART_THUMBS_TINY, True)
            return html.Div([
                render_frame_header(frame_no, aligned_frame_no),
                html.Div(legend, style={'float': 'right'}),
                dash_table.DataTable(
                    id='pixel-table-1',
                    columns=[
                                {'name': '', 'id': 'angles_tiny', 'presentation': 'markdown'}] + [
                                {
                                    'name': '',
                                    'id': i,
                                    'type': 'numeric',
                                    'format': Format(precision=0, scheme=Scheme.fixed),
                                } for i in df_angles.iloc[:, 3:].columns],
                    data=df_angles.to_dict('records'),
                    fixed_columns={'headers': True, 'data': 1},
                    css=[{
                        'selector': '.dash-spreadsheet tr',
                        'rule': '''
                        max-height: 13px; min-height: 13px; height: 13px;
                        display: block;
                        overflow-y: hidden;
                    '''
                    }],
                    style_data={'font-size': '0px', 'text-align': 'center', 'lineHeight': '1px'},
                    style_table={'max-width': '100%', 'min-width': '100%'},
                    style_cell={'max-width': '15px', 'min-width': '15px', 'width': '15px'},
                    style_data_conditional=styles,
                    tooltip_data=tooltip_angles(type='angles_small'),
                    tooltip_delay=0,
                    tooltip_duration=None,
                ),
            ])
        # Difference table case
        elif dif_table == 'true':
            styles_header = []
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
                    selected_row_ids=selected_rows,
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
                html.Div(legend, style={'float': 'right'}),
                dash_table.DataTable(
                    id={'type': 'datatable', 'id': 'table-tab2-main'},
                    columns=[
                                {'name': 'angles', 'id': 'angles', 'presentation': 'markdown'}] + [
                                {'name': 'id', 'id': 'id'}] + [
                                {
                                    'name': i,
                                    'id': i,
                                    'type': 'numeric',
                                    'format': Format(precision=2, scheme=Scheme.fixed),
                                } for i in df_angles.iloc[:, 2:].columns],
                    data=custom_sort_by(selected_rows, df_angles.to_dict('records')),
                    fixed_columns={'headers': True, 'data': 1},
                    style_cell={'font-size': '18px', 'text-align': 'center',
                                'p': {'margin-block-start': '0px', 'margin-block-end': '0px'},'fontWeight': 'bold'},
                    style_table={'overflowX': 'scroll', 'max-width': '100%'},
                    style_header={
                        'fontWeight': 'bold'
                    },
                    row_selectable='multi',
                    selected_row_ids=selected_rows,
                    sort_action='custom',
                    page_size=pagesize,
                    style_header_conditional=styles_header,
                    style_data_conditional=styles,
                    tooltip_data=tooltip_angles(),
                    tooltip_delay=0,
                    tooltip_duration=None,
                ),
            ])
    except Exception as e:
        print(e)
        return dash.no_update


def render_frame_header(frame_no, aligned_frame_no=[]):
    if frame_no != 'false' and not aligned_frame_no:
        return html.H4('Current Frame: #{}'.format(frame_no), style={'marginTop': '1%'})
    elif frame_no != 'false' and aligned_frame_no:
        element = html.Div([
            html.H4('Current Frame: #{}'.format(frame_no), style={'marginTop': '1%', 'display': 'inline'}),
            html.H4('Aligned Frame: {}'.format(aligned_frame_no), style={'marginTop': '1%', 'marginLeft': '4%','display': 'inline', 'color': 'red'})
            ])
        return element

    else: return html.H4()

def render_similarity_row(df_similarity):
    layout = html.Div()
    return layout

def custom_sort_by(selected_row_ids, data):
    selected_row_ids.sort()
    for i in range(len(selected_row_ids)):
        row = selected_row_ids[i]
        index = next((j for j, item in enumerate(data) if item['id'] == row), -1)
        data.insert(i, data.pop(index))
    derived_virtual_selected_rows = [i for i in range(len(selected_row_ids))]

    return data


def compute_styles(df_angles, frame_no, selected_rows, colormap, aligned_frame_no=[]):
    (styles, legend) = heatmap_table_format(df_angles, selected_rows=selected_rows, colormap=colormap)
    styles_header = []
    if frame_no != 'false':
        styles_header, extra_styles = highlight_current_frame(frame_no)
        styles.append(extra_styles)
    if aligned_frame_no:
        extra_styles_header, extra_styles = highlight_aligned_frame(aligned_frame_no)
        styles_header.append(extra_styles_header)
        styles = styles + extra_styles
    return styles
