# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 08:03:50 2022

@author: 500585
"""
import streamlit as st
from stuetzkraft_plot import topview_plot, sideview_plot, supports_bar_plot
from stuetzkraft_model_plain import results_plain
from stuetzkraft_helpers import xy_load
import pandas as pd
import loadcases

def _update_slider(slider_keys, values):
    for k, v in zip(slider_keys, values):
        st.session_state[k] = v

ini, lim = loadcases.elast()

# Initialize session state
for key in ini:
    if key not in st.session_state:
        st.session_state[key] = ini[key]

# Compute fixed ranges
range_x = [-ini['x23']*1.5, ini['x23']*1.5]
range_y = [-max(ini['y3'], ini['y4'])*1.5, max(ini['y1'], ini['y2'])*1.5]

# Start layouting
# Set wide mode by default
st.set_page_config(layout='wide')

st.title('Stützkraftverteilung')
st.sidebar.header('Load parameters')

# Create sliders in sidebar (Loads)
fl = st.sidebar.slider('z load force (fl)', min_value=lim['fl_min'], max_value=lim['fl_max'], value=ini['fl'], step=1., key='sl-fl')
ml = st.sidebar.slider('Load moment from boom (ml)', lim['ml_min'], lim['ml_max'], ini['ml'], key='sl-ml')
phi_deg_boom = st.sidebar.slider('Boom angle (phi_deg_boom)', lim['phi_deg_boom_min'], lim['phi_deg_boom_max'], ini['phi_deg_boom'], step=1., key='sl-pdb')

# Reset button
st.sidebar.button("Reset Loads",
                  on_click=_update_slider,
                  kwargs={'slider_keys': ['sl-fl', 'sl-ml', 'sl-pdb'], 
                          'values': [ini['fl'], ini['ml'], ini['phi_deg_boom']]}
                  )

# Compute loads from input
phi_deg_load = phi_deg_boom + 90.
mlx, mly = xy_load(ml, phi_deg_load)

# Create sliders in sidebar (Geometry)
st.sidebar.header('Geometry parameters')

y1 = st.sidebar.slider('Support A (y1)', lim['y_min'], lim['y_max'], ini['y1'], key='sl-y1')
y2 = st.sidebar.slider('Support B (y2)', lim['y_min'], lim['y_max'], ini['y2'], key='sl-y2')
y3 = st.sidebar.slider('Support C (y3)', lim['y_min'], lim['y_max'], ini['y3'], key='sl-y3')
y4 = st.sidebar.slider('Support D (y4)', lim['y_min'], lim['y_max'], ini['y4'], key='sl-y4')
x14 = st.sidebar.slider('Distance Front – Ring (x14)', lim['x_min'], lim['x_max'], ini['x14'], key='sl-x14')
x23 = st.sidebar.slider('Distance Rear – Ring (x23)', lim['x_min'], lim['x_max'], ini['x23'], key='sl-x23')

# Reset button
st.sidebar.button("Reset Geometry",
                  on_click=_update_slider,
                  kwargs={'slider_keys': ['sl-y1', 'sl-y2', 'sl-y3', 'sl-y4', 'sl-x14', 'sl-x23'], 
                          'values': [ini['y1'], ini['y2'], ini['y3'], ini['y4'], ini['x14'], ini['x23']]}
                  )

# Create sliders in sidebar (Springs)
st.sidebar.header('Hooke parameters')
d14 = st.sidebar.slider('Torsion spring rate front (d14)', lim['dt_min'], lim['dt_max'], ini['d14'], 100., key='sl-d14')
d23 = st.sidebar.slider('Torsion spring rate rear (d23)', lim['dt_min'], lim['dt_max'], ini['d23'], 100., key='sl-d23')
d1 = st.sidebar.slider('Compression spring rate @ ABCD (d1...d4)', lim['d_min'], lim['d_max'], ini['d1'], 100., key='sl-d1')
d2 = d1
d3 = d1
d4 = d1

# Reset button
st.sidebar.button("Reset Springs",
                  on_click=_update_slider,
                  kwargs={'slider_keys': ['sl-d14', 'sl-d23', 'sl-d1'], 
                          'values': [ini['d14'], ini['d23'], ini['d1']]}
                  )

# Compute new figures
inputs = {'fl': fl, 'mlx': mlx, 'mly': mly, 'x14': x14, 'x23': x23, 'd14': d14, 'd23': d23, 'd1': d1, 'd2': d2, 'd3': d3, 'd4': d4, 'y1': y1, 'y2': y2, 'y3': y3, 'y4': y4}
results = results_plain(fl, mlx, mly, y1, y2, y3, y4, x14, x23, d14, d23, d1, d2, d3, d4)

data = inputs | results  # Merge dicts (>= python 3.9.0)

df = pd.DataFrame(data, index=[0])

# Check if elastostatic model is valid
if any(s < 0 for s in [results['s1'], results['s2'], results['s3'], results['s4']]):
    st.warning('Mindestens eine Stütze hebt ab. Elastostatisches Modell ungültig! Dargestellte Werte ungültig!')

fig_top = topview_plot(data, range_x, range_y)
fig_side1 = sideview_plot(data, 'xz')
fig_side2 = sideview_plot(data, 'yz')
fig_bar = supports_bar_plot(data)

# Create Central Layout
st.subheader('Results')
res_df = pd.DataFrame(results, index=['Value'])
st.dataframe(res_df)

# Define ROW 1
# c12 = Row 1, Column 2
c11, c12 = st.columns([3, 1])

with c11:
    st.subheader('Top view')
    st.plotly_chart(fig_top, use_container_width=True)
        
with c12:
    st.subheader('Support deflections')
    st.plotly_chart(fig_bar, use_container_width=True)  

# Define ROW 2
c21, c22 = st.columns([1, 1])

with c21:
    st.subheader('Side view (XZ)')
    st.plotly_chart(fig_side1, use_container_width=True)
    
with c22:
    st.subheader('Front view (YZ)')
    st.plotly_chart(fig_side2, use_container_width=True)


    