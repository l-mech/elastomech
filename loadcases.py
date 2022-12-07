# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 08:42:26 2022

@author: 500585
"""

def elast():
    # Initial values
    ini = {  # Lasten
        'fl': 64305.4,  # N
        'ml': 149105.7,  # Nm
        'phi_deg_load': 60.,  # deg
        # mlx: 74552.9  # Nm
        # mly: 129129.3  # Nm 
        #Geometrie
        'h': 3.000,  # m
        'x14': 4.805,  # m
        'x23': 0.780,  # m
        # Federraten
        'd14': 30230370.0,  # Nm/rad
        'd23': 155189025.3,  # Nm/rad
        'd1': 3001412.8,  # N/m
        'd2': 3001412.8,  # N/m
        'd3': 3001412.8,  # N/m
        'd4': 3001412.8,  # N/m
        }
    
    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    
    # Boom angle
    ini['phi_deg_boom'] = ini['phi_deg_load'] - 90.
    
    lim = {  # Parametergrenzen
        # Stützen
        'y_min': 0.,
        'y_max': 4.,
        'x_min': 0.,
        'x_max': 8.,
        # Drehfedern
        'dt_min': 0.,
        'dt_max': 999999999.,
        # Druckfedern
        'd_min': 0.,
        'd_max': 999999999.,
        # Loads
        'fl_min': 0.,
        'fl_max': 500000.,
        'ml_min': 0.,
        'ml_max': 500000.,
        # Angles
        'phi_deg_boom_min': 0.,
        'phi_deg_boom_max': 360.
        }
    
    return ini, lim

def liftoff():
    # Initial values
    ini = {  # Lasten
        'fl': 64305.4,  # N
        'ml': 150000.0,  # Nm
        'phi_deg_load': 180.,  # deg
        #Geometrie
        'h': 3.000,  # m
        'x14': 4.805,  # m
        'x23': 0.780,  # m
        # Federraten
        'd14': 30230370.0,  # Nm/rad
        'd23': 155189025.3,  # Nm/rad
        'd1': 3001412.8,  # N/m
        'd2': 3001412.8,  # N/m
        'd3': 3001412.8,  # N/m
        'd4': 3001412.8,  # N/m
        }
    
    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    
    # Boom angle
    ini['phi_deg_boom'] = ini['phi_deg_load'] - 90.
    
    lim = {  # Parametergrenzen
        # Stützen
        'y_min': 0.,
        'y_max': 4.,
        'x_min': 0.,
        'x_max': 8.,
        # Drehfedern
        'dt_min': 0.,
        'dt_max': 999999999.,
        # Druckfedern
        'd_min': 0.,
        'd_max': 999999999.,
        # Loads
        'fl_min': 0.,
        'fl_max': 500000.,
        'ml_min': 0.,
        'ml_max': 500000.,
        # Angles
        'phi_deg_boom_min': 0.,
        'phi_deg_boom_max': 360.
        }
    
    return ini, lim