import plotly.graph_objects as go
from utils import COLORS, PAIRS_RENDER, BODY_SEGMENTS
import numpy as np


def render_stick_figure_init(df):
    fig = go.Figure()
    img_width_min = df.x[df.x != 0].min()
    img_height = round(df.y.max())
    # img_width = 400
    # img_width = 400
    # img_height = 400
    scale_factor = 0.5
    # fig.add_layout_image(
    #     x= round(df.x.min()) - 100,
    #     sizex=round(df.x.max()) + 200,
    #     y=100,
    #     sizey=img_height + 200,
    #     xref="paper",
    #     yref="y",
    #     opacity=1.0,
    #     layer="below"
    # )
    fig.update_xaxes(
        showgrid=False,
        scaleanchor='y',
        range=(round(img_width_min) - 50, round(df.x.max()) + 50)
    )
    fig.update_yaxes(
        showgrid=False,
        range=(img_height + 20, 25)
    )

    for pair, color in zip(PAIRS_RENDER, COLORS):
        x1 = int(df.x[pair[0]])
        y1 = int(df.y[pair[0]])
        x2 = int(df.x[pair[1]])
        y2 = int(df.y[pair[1]])
        z1 = df.confidence[pair[0]]
        z2 = df.confidence[pair[1]]

        if x1 != 0 and x2 != 0 and y1 != 0 and y2 != 0:
            fig.add_shape(
                type='line', xref='x', yref='y',
                x0=x1, x1=x2, y0=y1, y1=y2, line_color=color, line_width=4
            )
            fig.add_shape(
                type='circle', xref='x', yref='y',
                x0=x1 - 3, y0=y1 - 3, x1=x1 + 3, y1=y1 + 3, line_color=color, fillcolor=color
            )
            fig.add_shape(
                type='circle', xref='x', yref='y',
                x0=x2 - 3, y0=y2 - 3, x1=x2 + 3, y1=y2 + 3, line_color=color, fillcolor=color
            )
            # Hover data
            fig.add_trace(
                go.Scatter(
                    x=[x1],
                    y=[y1],
                    showlegend=False,
                    marker_color=color,
                    name='',
                    text='Confidence:{:.2f}'.format(z2),
                    opacity=0,
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=[x2],
                    y=[y2],
                    showlegend=False,
                    marker_color=color,
                    name='',
                    text='Confidence:{:.2f}'.format(z2),
                    opacity=0,
                )
            )

    return fig

def render_stick_figure(df, video, no_highlight=False):
    # teams_list = sorted(teams_list, key=str.lower)
    default_linewidth = 2
    highlighted_linewidth = 3
    fig = go.Figure()
    fig.layout.hovermode = "closest"
    fig.layout.hoverdistance = 1  # ensures no "gaps" for selecting sparse data
    # fig.layout.plot_bgcolor='black'
    fig.layout.uirevision = video

    fig.layout.autosize = True
    img_width_min = df.x[df.x != 0].min()
    img_height = round(df.y.max())
    img_height_min = df.y[df.y != 0].min()
    # Background in stick figure
    # fig.add_layout_image(
    #     dict(
    #         source="assets/thumbnails/background.png",
    #         x=round(img_width_min) / 4,
    #         sizex=round(df.x.max()) ,
    #         y=img_height_min,
    #         sizey=img_height_min * 4,
    #         xref="x",
    #         yref="y",
    #         opacity=1.0,
    #         layer="below",
    #         sizing="stretch", )
    # )
    fig.update_xaxes(
        showgrid=False,
        scaleanchor='y',
        range=(round(img_width_min) - 50, round(df.x.max()) + 50)
    )
    fig.update_yaxes(
        showgrid=False,
        range=(img_height + 20, img_height_min - 20)
    )
    # fig.layout.config.edits = (dict({"legendPosition": True}))
    for body_segment, color in zip(BODY_SEGMENTS.items(), COLORS):
        h_color = color if no_highlight else 'gray'
        opacity = 1 if no_highlight else 0.6
        coords = body_segment[1]
        name = body_segment[0]
        x = df.x[coords]
        y = df.y[coords]
        z = df.confidence[coords]

        fig.add_trace(go.Scatter(x=x[x>0], # filtering out missing coordinates
                                 y=y[y>0],
                                 name=name,
                                 mode='lines+markers',
                                 # text=z,
                                 opacity=opacity,
                                 hoveron='points+fills',
                                 fill='toself',
                                 line={'width': 4, 'color': h_color},
                                 marker=dict(size=10, color=color),
                                 ))
    # fig.update_layout(
    #     xaxis=dict(
    #         tickmode='array',
    #         tickvals=[0, 29, 58, 87, 117, 146],
    #         ticktext=[2015, 2016, 2017, 2018, 2019, 2020]
    #     )
    # )

    # fig.update_yaxes(range=[1350, 1650])
    # f = go.FigureWidget(fig)

    # our custom event handler
    def update_trace(trace, points, selector):
        print('points: {}'.format(points))
        if len(points.point_inds) == 1:
            print('here?')
            i = points.trace_index
            for x in range(0, len(fig.data)):
                fig.data[x]['line']['color'] = 'grey'
                fig.data[x]['opacity'] = 0.3
                fig.data[x]['line']['width'] = default_linewidth
            # print('Correct Index: {}',format(i))
            fig.data[i]['line']['color'] = 'red'
            fig.data[i]['opacity'] = 1
            fig.data[i]['line']['width'] = highlighted_linewidth

    # we need to add the on_click event to each trace separately
    for i in range(0, len(fig.data)):
        fig.data[i].on_click(update_trace)

    return fig
