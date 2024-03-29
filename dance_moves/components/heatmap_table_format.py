import dash_html_components as html
from settings import BODYPART_INDEX

COLOR_DICT_4 = {
    'Sand' : [
        '#fbefcc',
        '#f9ccac',
        '#f4a688',
        '#e0876a',
    ],

    'Else' : [
        '#fef0d9',
        '#fdcc8a',
        '#fc8d59',
        '#d7301f',
    ],

    'Blue' : [
        '#ddeedd',
        '#bae4bc',
        '#7bccc4',
        '#2b8cbe',
    ],

    'Green' : [
        '#edf8fb',
        '#b2e2e2',
        '#66c2a4',
        '#238b45',
    ]
}

COLOR_DICT_8 = {
    'Sand': [
        '#8c510a',
        '#bf812d',
        '#dfc27d',
        '#f6e8c3',
        '#fbefcc',
        '#f9ccac',
        '#f4a688',
        '#e0876a',
    ],

    'Else': [
        '#8c510a',
        '#bf812d',
        '#dfc27d',
        '#f6e8c3',
        '#fef0d9',
        '#fdcc8a',
        '#fc8d59',
        '#d7301f',
    ],

    'Blue': [
        '#8c510a',
        '#bf812d',
        '#dfc27d',
        '#f6e8c3',
        '#ddeedd',
        '#bae4bc',
        '#7bccc4',
        '#2b8cbe',
    ],

    'Green': [
        '#8c510a',
        '#bf812d',
        '#dfc27d',
        '#f6e8c3',
        '#edf8fb',
        '#b2e2e2',
        '#66c2a4',
        '#238b45',
    ]
}



def heatmap_table_format(df, n_bins=4, columns='all', selected_rows=[], colormap = 'Else', similarity = 'angle'):

    colormap = COLOR_DICT_8[colormap] if similarity == 'velocity' else COLOR_DICT_4[colormap]
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = 180
    df_min = 0.01
    if similarity == 'velocity':
        bounds = [i * (1.0 / 8) for i in range(8 + 1)]
        df_max = 180
        df_min = -180
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colormap[i-1]
        color = 'black' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color,
            })
            styles.append({
                'if': {
                    'filter_query': (
                            '{{{column}}} >= -0.45' +
                            ' && {{{column}}} <= 0.45'
                    ).format(column=column),
                    'column_id': column
                },
                'backgroundColor': 'white',
                'color': color,
            })
        for row in selected_rows:
            styles.append({
                'if': {
                    'column_id': 'angles',
                    'filter_query': '{{id}} = {}'.format(str(row)),
                },
                'border': '4px rgb(50, 50, 50) solid'
            })

        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )
    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))


def highlight_current_frame(frame_no):
    header_styles = []
    header_styles.append({
        'if': { 'column_id': 'Frame:{}'.format(frame_no), 'header_index': 0 },
        'color': 'white',
        'backgroundColor': 'black',
        'border': '3px black solid'
    })
    styles = {'if': {'column_id': 'Frame:{}'.format(frame_no), }, 'border-right': '3px black solid', 'border-left': '3px black solid'}
    return header_styles, styles


def highlight_aligned_frame(aligned_frame_no):
    header_styles = []
    styles = []
    for frame in aligned_frame_no:
        header_styles.append({
            'if': { 'column_id': 'Frame:{}'.format(frame), 'header_index': 0 },
            'color': 'white',
            'backgroundColor': 'red',
            'border': '3px red solid'
        })
        styles.append({'if': {'column_id': 'Frame:{}'.format(frame), }, 'border-right': '3px red solid', 'border-left': '3px red solid'})
    return header_styles, styles

def tooltip_angles(bodyparts=BODYPART_INDEX, type='angles'):
    tooltip = []
    for key, value in BODYPART_INDEX.items():
        tooltip.append({type: value})
    return tooltip
