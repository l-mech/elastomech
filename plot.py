# -*- coding: utf-8 -*-
"""Plot methods to create the figures for the dashboards using plotly."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from model_plain import results_plain
import numpy as np
import plotly.io as pio
from helpers import rotate, cart2pol


def load_arrow(mlx, mly, df_supports):
    """Return arrow components of rescaled arrow, so it always lies within fig boundaries."""
    x_max = df_supports['x'].max()
    x_min = df_supports['x'].min()
    y_max = df_supports['y'].max()
    y_min = df_supports['y'].min()

    min_dim = min(abs(x_max), abs(x_min), abs(y_max), abs(y_min)) * 2.5

    arrow_x = mlx
    arrow_y = mly

    max_arrow = max(abs(arrow_x), abs(arrow_y))

    if max_arrow > min_dim:
        scale = min_dim / max_arrow
        arrow_x = arrow_x * scale
        arrow_y = arrow_y * scale

    return arrow_x, arrow_y


def results_plot(datasets, x_label, y_label, title="", xformat='.1f', yformat=',.1f'):
    """Return plotly figure to show computation results."""
    fig = go.Figure()

    for (x, y) in datasets:

        fig.add_trace(
            go.Scatter(x=x,
                       y=y,
                       mode='lines+markers',
                       name=y.name))

    # Tight layout, labels, etc.
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      xaxis_title=x_label,
                      yaxis_title=y_label,
                      # paper_bgcolor="LightSteelBlue",
                      # legend_title_text='',
                      xaxis_tickformat=xformat,  # https://d3-wiki.readthedocs.io/zh_CN/master/Formatting/#numbers
                      yaxis_tickformat=yformat,
                      title=title,
                      )

    # fig = go.FigureWidget(fig)

    return fig


def topview_plot(d, range_x, range_y):
    """Return plotly figure for Support Force Distribution's Top view plot."""
    ax = d['x14']
    bx = -d['x23']
    cx = -d['x23']
    dx = d['x14']

    ay = d['y1']
    by = d['y2']
    cy = -d['y3']
    dy = -d['y4']

    az = -d['s1']
    bz = -d['s2']
    cz = -d['s3']
    dz = -d['s4']

    f1 = d['f1']
    f2 = d['f2']
    f3 = d['f3']
    f4 = d['f4']

    supports = [[ax, ay, az, f1],
                [bx, by, bz, f2],
                [cx, cy, cz, f3],
                [dx, dy, dz, f4]]

    df_supports = pd.DataFrame(supports,
                               columns=['x', 'y', 'z', 'f'],
                               index=['A', 'B', 'C', 'D'])

    # General plot style settings
    template = 'seaborn'  # 'seaborn', 'plotly_white', 'ggplot2', 'plotly_dark', 'presentation' (also: 'plotly+presentation')
    linecolor = 'black'
    loadcolor = 'red'
    geocolor = 'blue'

    # Support forces scatter plot
    # Replace all negative values in size by zero to prevent exception.
    size = df_supports['f'].copy()
    size = size.clip(lower=0)

    fig = px.scatter(df_supports,
                     x='x',
                     y='y',
                     size=size,
                     # size_max=120,
                     color=df_supports.index,
                     text=[f'F = {val:.1f}' for val in df_supports['f']],
                     template=template,
                     range_x=range_x,
                     range_y=range_y)

    # Add decoration lines
    trace_ad = go.Scatter(
        x=[df_supports.loc['A', 'x'],
           df_supports.loc['D', 'x']],
        y=[df_supports.loc['A', 'y'],
           df_supports.loc['D', 'y']],
        line=dict(color=linecolor),
        showlegend=False)

    trace_bc = go.Scatter(
        x=[df_supports.loc['B', 'x'],
           df_supports.loc['C', 'x']],
        y=[df_supports.loc['B', 'y'],
           df_supports.loc['C', 'y']],
        line=dict(color=linecolor),
        showlegend=False)

    trace_mid = go.Scatter(
        x=[max(df_supports.loc['A', 'x'], df_supports.loc['D', 'x']),
           min(df_supports.loc['B', 'x'], df_supports.loc['C', 'x'])],
        y=[0., 0.],
        line=dict(color=linecolor),
        showlegend=False)

    trace_center = go.Scatter(x=[0.],
                              y=[0.],
                              mode='markers',
                              # marker_size=50,
                              marker_color=linecolor,
                              showlegend=False)

    trace_deadweight = go.Scatter(x=[d['xe']],
                                  y=[0.],
                                  mode='markers+text',
                                  # marker_size=[d['fe']],
                                  marker_color=loadcolor,
                                  text='Dead weight (fe)',
                                  showlegend=False)

    fig.add_trace(trace_ad)
    fig.add_trace(trace_bc)
    fig.add_trace(trace_mid)
    fig.add_trace(trace_center)
    fig.add_trace(trace_deadweight)

    arr_x, arr_y = load_arrow(d['mlx'], d['mly'], df_supports)

    boom_x, boom_y = rotate(np.asarray([arr_x, arr_y]), -np.pi / 2.)

    # Add load moment vector arrow
    # Arrow is reversed in order to have text label show up at arrow tip. Hence
    # arrowside='start'
    fig.add_annotation(x=0.,  # arrows' head
                       y=0.,  # arrows' head
                       ax=arr_x,  # arrows' tail
                       ay=arr_y,  # arrows' tail
                       xref='x',
                       yref='y',
                       axref='x',
                       ayref='y',
                       text='Load moment (ml)',
                       showarrow=True,
                       arrowhead=2,
                       arrowsize=1,
                       arrowwidth=2,
                       arrowcolor=loadcolor,
                       arrowside='start',
                       # xanchor='left'
                       )

    # Add boom arrow
    fig.add_annotation(x=0.,  # arrows' head
                       y=0.,  # arrows' head
                       ax=boom_x,  # arrows' tail
                       ay=boom_y,  # arrows' tail
                       xref='x',
                       yref='y',
                       axref='x',
                       ayref='y',
                       text='Boom',  # if you want only the arrow
                       showarrow=True,
                       arrowhead=7,
                       arrowsize=1,
                       arrowwidth=2,
                       arrowcolor=geocolor,
                       arrowside='start')

    # Set text label positions
    fig.update_traces(textposition='top center')

    # Scale x:y 1:1
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    # Title
    # fig.update_layout(title='Supports (positions/forces)')

    # Legend title
    fig.update_layout(legend_title_text='')

    # Tight layout
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      # paper_bgcolor="LightSteelBlue",
                      )

    # Construct FigureWidget from graph object

    # fig = go.FigureWidget(fig)

    return fig


def support_plot_3d(d):
    """Return plotly figure for Support Force Distribution's 3D plot."""
    ax = d['x14']
    bx = -d['x23']
    cx = -d['x23']
    dx = d['x14']

    ay = d['y1']
    by = d['y2']
    cy = -d['y3']
    dy = -d['y4']

    az = -d['s1']
    bz = -d['s2']
    cz = -d['s3']
    dz = -d['s4']

    supports = [[ax, ay, az],
                [bx, by, bz],
                [cx, cy, cz],
                [dx, dy, dz]]

    df_supports = pd.DataFrame(supports,
                               columns=['x', 'y', 'z'],
                               index=['A', 'B', 'C', 'D'])

    # General plot style settings
    template = 'seaborn'  # 'seaborn', 'plotly_white', 'ggplot2', 'plotly_dark', 'presentation' (also: 'plotly+presentation')
    linecolor = 'black'

    # Support forces scatter plot
    fig = px.scatter_3d(df_supports,
                        x='x',
                        y='y',
                        z='z',
                        # size_max=120,
                        # title='Supports (positions)',
                        color=df_supports.index,
                        template=template)

    # Add decoration lines
    trace_ad = go.Scatter3d(
        x=[df_supports.loc['A', 'x'],
           df_supports.loc['D', 'x']],
        y=[df_supports.loc['A', 'y'],
           df_supports.loc['D', 'y']],
        z=[df_supports.loc['A', 'z'],
           df_supports.loc['D', 'z']],
        line=dict(color=linecolor),
        showlegend=False,
        mode='lines')

    trace_bc = go.Scatter3d(
        x=[df_supports.loc['B', 'x'],
           df_supports.loc['C', 'x']],
        y=[df_supports.loc['B', 'y'],
           df_supports.loc['C', 'y']],
        z=[df_supports.loc['B', 'z'],
           df_supports.loc['C', 'z']],
        line=dict(color=linecolor),
        showlegend=False,
        mode='lines')

    trace_mid = go.Scatter3d(
        x=[(df_supports.loc['A', 'x'] + df_supports.loc['D', 'x']) / 2.,
           (df_supports.loc['B', 'x'] + df_supports.loc['C', 'x']) / 2.],
        y=[(df_supports.loc['A', 'y'] + df_supports.loc['D', 'y']) / 2.,
           (df_supports.loc['B', 'y'] + df_supports.loc['C', 'y']) / 2.],
        z=[(df_supports.loc['A', 'z'] + df_supports.loc['D', 'z']) / 2.,
           (df_supports.loc['B', 'z'] + df_supports.loc['C', 'z']) / 2.],
        line=dict(color=linecolor),
        showlegend=False,
        mode='lines')

    fig.add_trace(trace_ad)
    fig.add_trace(trace_bc)
    fig.add_trace(trace_mid)

    # Add zero plane
    x = [ax, bx, cx, dx]
    y = [ay, by, cy, dy]
    z = [[0, 0., 0., 0.],
         [0, 0., 0., 0.],
         [0, 0., 0., 0.],
         [0, 0., 0., 0.]]

    fig.add_trace(
        go.Surface(
            x=x,
            y=y,
            z=z,
            showscale=False,
            opacity=0.2,
            name='z-Plane (zero deflection)',
            showlegend=True))

    # Legend title
    fig.update_layout(legend_title_text='')

    # Scale x:y 1:1
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    # Construct FigureWidget from graph object

    # fig = go.FigureWidget(fig)

    return fig


def topview_plot_ro_polar(d, d_ro, mode='lines+markers'):
    """Return plotly figure for Working Radius' polar plot."""
    ax = d['x14']
    bx = -d['x23']
    cx = -d['x23']
    dx = d['x14']

    ay = d['y1']
    by = d['y2']
    cy = -d['y3']
    dy = -d['y4']

    supports_polar = [cart2pol(ax, ay),  # Returns r, theta (in rad!)
                      cart2pol(bx, by),
                      cart2pol(cx, cy),
                      cart2pol(dx, dy)]

    df_supports = pd.DataFrame(supports_polar,
                               columns=['r', 'theta'],
                               index=['A', 'B', 'C', 'D'])

    # px.scatter_ploar needs degrees
    df_supports['theta'] = np.rad2deg(df_supports['theta'])

    df_ro = pd.DataFrame(d_ro,
                         columns=['ro', 'phi'])

    # General plot style settings
    template = 'seaborn'  # 'seaborn', 'plotly_white', 'ggplot2', 'plotly_dark', 'presentation' (also: 'plotly+presentation')
    linecolor = 'grey'
    loadcolor = 'red'
    # geocolor = 'blue'
    rocolor = 'salmon'

    r_max = df_ro['ro'].max()

    # Position of supports in polar scatter plot
    fig = px.scatter_polar(df_supports,
                           r='r',
                           theta='theta',
                           color=df_supports.index,
                           template=template,
                           start_angle=0,
                           direction='counterclockwise',
                           range_r=[0., r_max * 1.1])

    # Add decoration lines
    # A--D
    fig.add_trace(
        go.Scatterpolar(
            r=[df_supports.loc['A', 'r'],
               df_supports.loc['D', 'r']],
            theta=[df_supports.loc['A', 'theta'],
                   df_supports.loc['D', 'theta']],
            mode='lines',
            line=dict(color=linecolor),
            showlegend=False))
    # B--C
    fig.add_trace(
        go.Scatterpolar(
            r=[df_supports.loc['B', 'r'],
               df_supports.loc['C', 'r']],
            theta=[df_supports.loc['B', 'theta'],
                   df_supports.loc['C', 'theta']],
            mode='lines',
            line=dict(color=linecolor),
            showlegend=False))

    # Midline
    xv = max(ax, dx)
    xh = min(bx, cx)
    rv = cart2pol(xv, 0.)[0]
    rh = cart2pol(xh, 0.)[0]

    fig.add_trace(
        go.Scatterpolar(
            r=[rv, rh],
            theta=[0., 180.],
            mode='lines',
            line=dict(color=linecolor),
            opacity=1.,
            showlegend=False))

    # Working Radius as scatter plot
    fig.add_trace(
        go.Scatterpolar(
            r=df_ro['ro'],
            theta=df_ro['phi'],
            mode=mode,
            name='Max Reachout',
            line_color=rocolor,
            thetaunit='degrees'))

    # Marker for center
    fig.add_trace(
        go.Scatterpolar(
            r=[0.],
            theta=[0.],
            mode='markers',
            marker_color=linecolor,
            showlegend=False))

    # Marker for dead weight position
    fig.add_trace(
        go.Scatterpolar(
            r=[d['xe']],
            theta=[0.],
            mode='markers+text',
            marker_color=loadcolor,
            text='Dead weight (fe)',
            showlegend=False))

    # Set text label positions
    fig.update_traces(textposition='top center')

    # Legend title
    fig.update_layout(legend_title_text='')

    # Tight layout
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      # paper_bgcolor="LightSteelBlue",
                      template=template
                      )

    # Construct FigureWidget from graph object

    # fig = go.FigureWidget(fig)

    return fig


def sideview_plot(d, plane, proj_type='perspective'):
    """
    Return plotly figure for Support Force Distribution's 3D side view plot.

    Parameters
    ----------
    d : dict
        Data.
    plane : string
        'xz', 'yz' or 'xy'
    proj_type : string, optional
        Set projection type to either 'orthographic' or 'perspective'.
        The default is 'perspective'.

    Returns
    -------
    fig : plotly figure object
    """
    fig = support_plot_3d(d)

    eye_zoom = 2.0

    if plane == 'xz':
        x = 0.
        y = eye_zoom
        z = 0.

    elif plane == 'yz':
        x = eye_zoom
        y = 0.
        z = 0.

    elif plane == 'xy':
        x = 0.
        y = 0.
        z = eye_zoom
    else:
        raise ValueError

    # Set camera to plane
    # https://plotly.com/python/3d-camera-controls/
    camera = dict(up=dict(x=0, y=0, z=1),  # z points up
                  eye=dict(x=x, y=y, z=z),  # camera position
                  center=dict(x=0, y=0, z=0),
                  projection=dict(type=proj_type))

    fig.update_layout(scene_camera=camera)

    # fig.update_layout(title='Supports (side view)')

    # Tight layout
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      # paper_bgcolor="LightSteelBlue",
                      )

    return fig


def supports_bar_plot(d):
    """Return plotly figure for Support Force Distribution's bar plot."""
    supports = [[d['s1']],
                [d['s2']],
                [d['s3']],
                [d['s4']]]

    df_supports = pd.DataFrame(supports,
                               columns=['s'],
                               index=['A', 'B', 'C', 'D'])

    fig = px.bar(df_supports,
                 x=df_supports.index,
                 y='s',
                 color=df_supports.index,
                 labels={'index': '', 's': 'Deflection'})

    # Hide legend
    fig.update_layout(showlegend=False)

    # Tight layout
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                      # paper_bgcolor="LightSteelBlue",
                      )

    return fig


if __name__ == "__main__":

    pio.renderers.default = 'browser'

    # Lasten
    fl = 64305.4  # N
    mlx = 74552.9  # Nm
    mly = 129129.3  # Nm

    # Geometrie
    h = 3.000  # m
    x14 = 4.805  # m
    x23 = 0.780  # m

    # Federraten
    d14 = 30230370.0  # Nm/rad
    d23 = 155189025.3  # Nm/rad
    d1 = 3001412.8  # N/m
    d2 = 3001412.8  # N/m
    d3 = 3001412.8  # N/m
    d4 = 3001412.8  # N/m

    # Symmetrie
    y1 = h
    y2 = h
    y3 = h
    y4 = h

    range_x = [-x23 * 1.5, x23 * 1.5]
    range_y = [-max(y3, y4) * 1.5, max(y1, y2) * 1.5]

    inputs = {'fl': fl, 'mlx': mlx, 'mly': mly, 'h': h, 'x14': x14, 'x23': x23, 'd14': d14, 'd23': d23, 'd1': d1, 'd2': d2, 'd3': d3, 'd4': d4, 'y1': y1, 'y2': y2, 'y3': y3, 'y4': y4}
    results = results_plain(fl, mlx, mly, y1, y2, y3, y4, x14, x23, d14, d23, d1, d2, d3, d4)

    data = inputs | results  # Merge dicts (>= python 3.9.0)

    df = pd.DataFrame(data, index=[0])

    fig1 = topview_plot(data, range_x, range_y)
    fig2 = sideview_plot(data, 'xz')
    fig3 = supports_bar_plot(data)

    fig1.show()
    fig2.show()
    fig3.show()
