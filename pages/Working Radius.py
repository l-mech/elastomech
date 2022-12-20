# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 08:03:50 2022

@author: 500585
"""
import streamlit as st
from stuetzkraft_plot import topview_plot_ro_polar, results_plot
from stuetzkraft_helpers import xy_load, case_dependent_results, limited_reachout, load_moment, check_liftoffs, restlast
import pandas as pd
import loadcases
from loadcases import lim_ro as lim
import numpy as np
import time
from Home import check_password

def _update_slider(slider_keys, values):
    for k, v in zip(slider_keys, values):
        st.session_state[k] = v

def grenzkurve(inputs):
    i = inputs      
    step = i['stepsize']
    mode='lines+markers'  
    j = 0
    step_array = np.arange(0., 360., step)
    progbar = st.progress(0)
   
    # Create dict of empty lists
    ks = ['phi', 'ro', 'ml', 'mlx', 'mly', 'lift id', 'Restlast key', 'Restlast val', 'f12', 'f23', 'f34', 'f14']
    res_ks = ['f1', 'f2', 'f3', 'f4', 'ffy', 'fry', 'phi1', 'phi2', 'phi3', 's1', 's2', 's3', 's4', 't14x', 't23x']
    d_ro = {}
    d_fails = {'phi': [],
               'msg': [],
               'No of iterations': [],
               'status': []}
    
    for k in ks + res_ks:
        d_ro[k] = []

    for phi in step_array:
        i['phi_deg_boom'] = phi
        i['phi_deg_load'] = phi + 90.
        res = limited_reachout(inputs)
        ro = float(res.x[0])  # Sanitize ro before using it further!
        if res.success:  # If optimization is successful
            ml = load_moment([(i['f_ro'], ro)])
            mlx, mly = xy_load(ml, i['phi_deg_load'])
            results, errors, warnings = case_dependent_results(i['fl'], mlx, mly, i['fe'], i['y1'], i['y2'], i['y3'], i['y4'], i['xe'], i['x14'], i['x23'], i['d14'], i['d23'], i['d1'], i['d2'], i['d3'], i['d4'])
            data = inputs | results
        
            _, lift_ids, _ = check_liftoffs(results)
            rl_min, rl = restlast(results)
            
            # Write freshly computed values to corresponding list in dict
            vs = [phi, ro, ml, mlx, mly, lift_ids, rl_min[0], rl_min[1], rl['f12'], rl['f23'], rl['f34'], rl['f14']]
            for k, v in zip(ks, vs):
                d_ro[k].append(v)
            # Do the same with values from results dict
            for k in res_ks:
                v = float(results[k])
                d_ro[k].append(v)
                
        else: # If optimization is NOT successful
            d_fails['phi'].append(phi)
            d_fails['msg'].append(res.message)
            d_fails['No of iterations'].append(res.nit)
            d_fails['status'].append(res.status)
            data = inputs
            mode = 'markers'
            
        print(f'j: {j}, phi: {phi}, ro: {ro}')
        
        j += 1
        progbar.progress(j/step_array.size)
     
    fig = topview_plot_ro_polar(d=data, d_ro=d_ro, mode=mode)
    
    return fig, d_ro, d_fails

if check_password():
    # Dashboard starts here
    ini, _ = loadcases.ro_default()
    export_dfs = []
    
    # Initialize session state
    for key in ini:
        if key not in st.session_state:
            st.session_state[key] = ini[key]
    
    # Start layouting
    # Set wide mode by default
    st.set_page_config(page_title='Working Radius',
                       page_icon="🔵",
                       layout='wide')
    
    st.title('Ausladungsgrenzen')# Placeholder for run settings
    inp_csv_placeholder = st.sidebar.empty()
    
    # Placeholder for run settings
    run_placeholder = st.sidebar.empty()
    
    # Create sliders in sidebar (Bounds)
    st.sidebar.header('Bounds')
    ro_lb, ro_ub = st.sidebar.slider('Ausladung min/max (ro)', min_value=lim['ro_min'], max_value=lim['ro_max'], value=(lim['ro_min'], lim['ro_max']), step=0.1, key='sl-ro')
    
    rl_lb, rl_ub = st.sidebar.slider('Restlast min/max (rl)', min_value=lim['rl_min'], max_value=lim['rl_max'], value=(lim['rl_min'], lim['rl_max']), step=1., key='sl-rl')
    
    f1_lb, f1_ub = st.sidebar.slider('Stützenkraft A min/max (f1)', min_value=lim['f1_min'], max_value=lim['f1_max'], value=(lim['f1_min'], lim['f1_max']), step=1., key='sl-f1')
    f2_lb, f2_ub = st.sidebar.slider('Stützenkraft B min/max (f2)', min_value=lim['f2_min'], max_value=lim['f2_max'], value=(lim['f2_min'], lim['f2_max']), step=1., key='sl-f2')
    f3_lb, f3_ub = st.sidebar.slider('Stützenkraft C min/max (f3)', min_value=lim['f3_min'], max_value=lim['f3_max'], value=(lim['f3_min'], lim['f3_max']), step=1., key='sl-f3')
    f4_lb, f4_ub = st.sidebar.slider('Stützenkraft D min/max (f4)', min_value=lim['f4_min'], max_value=lim['f4_max'], value=(lim['f4_min'], lim['f4_max']), step=1., key='sl-f4')
    
    t14x_lb, t14x_ub = st.sidebar.slider('Torsionsmoment vorne min/max (t14x)', min_value=lim['t14x_min'], max_value=lim['t14x_max'], value=(lim['t14x_min'], lim['t14x_max']), step=1., key='sl-t14x')
    t23x_lb, t23x_ub = st.sidebar.slider('Torsionsmoment hinten min/max (t23x)', min_value=lim['t23x_min'], max_value=lim['t23x_max'], value=(lim['t23x_min'], lim['t23x_max']), step=1., key='sl-t23x')
    
    # Reset button
    st.sidebar.button("Reset Limits",
                      on_click=_update_slider,
                      kwargs={'slider_keys': ['sl-ro', 'sl-rl', 'sl-f1', 'sl-f2', 'sl-f3', 'sl-f4', 'sl-t14x', 'sl-t23x'], 
                              'values': [
                                  (lim['ro_min'], lim['ro_max']),
                                  (lim['rl_min'], lim['rl_max']),
                                  (lim['f1_min'], lim['f1_max']),
                                  (lim['f2_min'], lim['f2_max']),
                                  (lim['f3_min'], lim['f3_max']),
                                  (lim['f4_min'], lim['f4_max']),
                                  (lim['t14x_min'], lim['t14x_max']),
                                  (lim['t23x_min'], lim['t23x_max']),
                                  ]}
                      )
    
    # Create sliders in sidebar (Loads)
    st.sidebar.header('Load parameters')
    fl = st.sidebar.slider('z Load force (fl)', min_value=lim['fl_min'], max_value=lim['fl_max'], value=ini['fl'], step=1., key='sl-fl')
    f_ro = st.sidebar.slider('Force at boom tip (f_ro)', lim['f_ro_min'], lim['f_ro_max'], ini['f_ro'], key='sl-fro')
    fe = st.sidebar.slider('Dead weight (fe)', min_value=lim['fe_min'], max_value=lim['fe_max'], value=ini['fe'], step=1., key='sl-fe')
    xe = st.sidebar.slider('Distance Ring – Dead weight (xe)', min_value=lim['xe_min'], max_value=lim['xe_max'], value=ini['xe'], key='sl-xe')
    
    # Reset button
    st.sidebar.button("Reset Loads",
                      on_click=_update_slider,
                      kwargs={'slider_keys': ['sl-fl', 'sl-fro', 'sl-fe', 'sl-xe'], 
                              'values': [ini['fl'], ini['f_ro'], ini['fe'], ini['xe']]}
                      )
    
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
    
    
    # Computing
    mlx = 0.
    mly = 0.
    
    inputs = {'fl': fl, 'mlx': mlx, 'mly': mly, 'fe': fe, 'xe': xe, 'x14': x14, 'x23': x23, 'd14': d14, 'd23': d23, 'd1': d1, 'd2': d2, 'd3': d3, 'd4': d4, 'y1': y1, 'y2': y2, 'y3': y3, 'y4': y4}
    
    inputs['f_ro'] = f_ro
    inputs['rl_lb'] = rl_lb
    inputs['rl_ub'] = rl_ub
    
    inputs['ro_lb'] = ro_lb
    inputs['ro_ub'] = ro_ub
    
    inputs['f1_lb'] = f1_lb
    inputs['f1_ub'] = f1_ub
    inputs['f2_lb'] = f2_lb
    inputs['f2_ub'] = f2_ub
    inputs['f3_lb'] = f3_lb
    inputs['f3_ub'] = f3_ub
    inputs['f4_lb'] = f4_lb
    inputs['f4_ub'] = f4_ub
    
    inputs['t14x_lb'] = t14x_lb
    inputs['t14x_ub'] = t14x_ub
    inputs['t23x_lb'] = t23x_lb
    inputs['t23x_ub'] = t23x_ub
    
    df_inputs = pd.DataFrame(inputs, index=np.arange(len(inputs)))
    
    with inp_csv_placeholder:
        inp_csv = df_inputs.to_csv(index=False).encode('utf-8')
        st.download_button(
           "Download Input values as csv",
           inp_csv,
           "Inputs_" + time.strftime("%Y%m%d-%H%M%S") + ".csv",
           "text/csv",
           key='dl-inp-csv')
       
    
    d_bounds = {'phi': [0., 360.],
                'rl lower bound': [rl_lb, rl_lb],
                'rl upper bound': [rl_ub, rl_ub],
                'f1 lower bound': [f1_lb, f1_lb],
                'f1 upper bound': [f1_ub, f1_ub],
                'f2 lower bound': [f2_lb, f2_lb],
                'f2 upper bound': [f2_ub, f2_ub],
                'f3 lower bound': [f3_lb, f3_lb],
                'f3 upper bound': [f3_ub, f3_ub],
                'f4 lower bound': [f4_lb, f4_lb],
                'f4 upper bound': [f4_ub, f4_ub],
                't14x lower bound': [t14x_lb, t14x_lb],
                't14x upper bound': [t14x_ub, t14x_ub],
                't23x lower bound': [t23x_lb, t23x_lb],
                't23x upper bound': [t23x_ub, t23x_ub],
                }
                
    
    df_bounds = pd.DataFrame.from_dict(d_bounds, orient='columns')
    
    results, _, _ = case_dependent_results(fl, mlx, mly, fe, y1, y2, y3, y4, xe, x14, x23, d14, d23, d1, d2, d3, d4)
    data = inputs | results
    
    d_ro = {'phi': [], 'ro': []}
    fig_ro = topview_plot_ro_polar(d=data, d_ro=d_ro)
    show_data = False
    
    export_dfs.extend((df_inputs))
    
    with run_placeholder.container():
        # Computation settings and Button
        st.subheader('Run Settings')
        stepsize = st.slider('Step size for φ (in deg)', 1, 15, 5, 1, key='sl-step')
        inputs['stepsize'] = stepsize
        
        if st.button('Grenzkurve ermitteln'):
            fig_ro, d_ro, d_fails = grenzkurve(inputs)
            df_ro = pd.DataFrame(d_ro, index=d_ro['phi'])
            df_fails = pd.DataFrame(d_fails, index=d_fails['phi'])
            
            show_data = True
            
    
    # Create Central Layout
    # Define ROW 1
    # c12 = Row 1, Column 2
    c11, c12 = st.columns([1, 2])
    with c11:
        st.subheader('Reachout(φ)')
        st.plotly_chart(fig_ro, use_container_width=True)
    
    if show_data:
        with c12:
            st.subheader('Result plots(φ)')
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Restlasten", "📈 Stützkräfte", "📈 Lastmomente", "📈 Rahmenmomente"])
            with tab1:
                fig_rl = results_plot([
                    (df_bounds['phi'], df_bounds['rl lower bound']),
                    (df_bounds['phi'], df_bounds['rl upper bound']),
                    (df_ro['phi'], df_ro['f12']),
                    (df_ro['phi'], df_ro['f23']),
                    (df_ro['phi'], df_ro['f34']),
                    (df_ro['phi'], df_ro['f14']),
                    ],
                    'φ in deg',
                    'Restlasten')
                st.plotly_chart(fig_rl, use_container_width=True)
                    
            with tab2:
                fig_f = results_plot([
                    (df_bounds['phi'], df_bounds['f1 lower bound']),
                    (df_bounds['phi'], df_bounds['f1 upper bound']),
                    (df_bounds['phi'], df_bounds['f2 lower bound']),
                    (df_bounds['phi'], df_bounds['f2 upper bound']),
                    (df_bounds['phi'], df_bounds['f3 lower bound']),
                    (df_bounds['phi'], df_bounds['f3 upper bound']),
                    (df_bounds['phi'], df_bounds['f4 lower bound']),
                    (df_bounds['phi'], df_bounds['f4 upper bound']),
                    (df_ro['phi'], df_ro['f1']),
                    (df_ro['phi'], df_ro['f2']),
                    (df_ro['phi'], df_ro['f3']),
                    (df_ro['phi'], df_ro['f4']),
                    ],
                    'φ in deg',
                    'Stützkräfte',)
                st.plotly_chart(fig_f, use_container_width=True)
            
            with tab3:
                fig_lm = results_plot([
                    (df_ro['phi'], df_ro['ml']),
                    (df_ro['phi'], df_ro['mlx']),
                    (df_ro['phi'], df_ro['mly']),
                    ],
                    'φ in deg',
                    'Lastmoment',)
                st.plotly_chart(fig_lm, use_container_width=True)   
         
            with tab4:
                fig_t = results_plot([
                    (df_bounds['phi'], df_bounds['t14x lower bound']),
                    (df_bounds['phi'], df_bounds['t14x upper bound']),
                    (df_bounds['phi'], df_bounds['t23x lower bound']),
                    (df_bounds['phi'], df_bounds['t23x upper bound']),
                    (df_ro['phi'], df_ro['t14x']),
                    (df_ro['phi'], df_ro['t23x']),
                    ],
                    'φ in deg',
                    'Drehmoment',)
                st.plotly_chart(fig_t, use_container_width=True)  
        
        if not df_fails.empty:
            st.subheader('Optimization errors')
            fails_csv = df_fails.to_csv(index=False).encode('utf-8')
            st.download_button(
               "Download Error log as csv",
               fails_csv,
               "Errors_" + time.strftime("%Y%m%d-%H%M%S") + ".csv",
               "text/csv",
               key='dl-fail-csv')
            st.dataframe(df_fails)
            st.warning('If no solution is found within the bounds, the script proceeds to the next value of phi.\n Missing solutions could be due to physically impossible bounds or in some cases due to the fact that the optimization algorithm (SLSQP) is not able to handle jumps between calculation models (e.g. change from an elastostatic model to a statically determinate model (three supports with ground contact)).')
        
        st.subheader('Full results')
        
        res_csv = df_ro.to_csv(index=False).encode('utf-8')
        st.download_button(
           "Download Results as csv",
           res_csv,
           "Results_" + time.strftime("%Y%m%d-%H%M%S") + ".csv",
           "text/csv",
           key='dl-res-csv')
            
        st.dataframe(df_ro)




   