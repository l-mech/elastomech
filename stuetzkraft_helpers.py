# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:05:53 2022

@author: 500585
"""
import numpy as np
from stuetzkraft_model_plain import results_plain, results_liftoff_plain
from scipy.optimize import minimize, shgo

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def case_dependent_results(fl, mlx, mly, fe, y1, y2, y3, y4, xe, x14, x23, d14, d23, d1, d2, d3, d4):
    # Initial run
    errors = []
    warnings = []
    results = results_plain(fl, mlx, mly, fe, y1, y2, y3, y4, xe, x14, x23, d14, d23, d1, d2, d3, d4)

    # Check if elastostatic model is valid
    # if any(f < 0 for f in [results['f1'], results['f2'], results['f3'], results['f4']]):
    count, lift_ids, _ = check_liftoffs(results)

    if count == 1:  # Genau eine Stütze hebt ab
        results = results_liftoff_plain(fl, mlx, mly, fe, y1, y2, y3, y4, xe, x14, x23, d14, d23, d1, d2, d3, d4, lift=lift_ids[0])
        count, lift_ids, warnings = check_liftoffs(results)

    if count > 1:  # Mehrere Stützen heben ab
        errors = ['Mehr als eine Stütze hebt ab. Berechnung ungültig.']
        
    return results, errors, warnings

def load_moment(force_distance_pairs):
    mls = []
    for (f, r) in force_distance_pairs:
        mls.append(f*r)
    ml = sum(mls)
    return ml

def restlast(results):
    f1, f2, f3, f4 = results['f1'], results['f2'], results['f3'], results['f4']
    f12 = f1+f2
    f23 = f2+f3
    f34 = f3+f4
    f14 = f1+f4
    ks = ['f12', 'f23', 'f34', 'f14']
    vls = [f12, f23, f34, f14]
    minpos = vls.index(min(vls))
    rl_min = (ks[minpos], vls[minpos])
    rl = {'f12': f12, 'f23': f23, 'f34': f34, 'f14': f14}
    return rl_min, rl
    

def limited_reachout(inputs):
    
    def results_by_ro(ro, inputs):
        i = inputs
        ml = load_moment([(i['f_ro'], ro)])
        mlx, mly = xy_load(ml, i['phi_deg_load'])
        results, _, _ = case_dependent_results(i['fl'], mlx, mly, i['fe'], i['y1'], i['y2'], i['y3'], i['y4'], i['xe'], i['x14'], i['x23'], i['d14'], i['d23'], i['d1'], i['d2'], i['d3'], i['d4'])
        return results
    
    def restlast_by_ro(ro, inputs):
        results = results_by_ro(ro, inputs)
        (_, restl_v), _ = restlast(results)
        return restl_v

    def restlast_constraint_lb(ro, inputs):
        # Randbedingung: rl_lb <= restlast(ro)
        return restlast_by_ro(ro, inputs)-inputs['rl_lb']
    
    def restlast_constraint_ub(ro, inputs):
        # Randbedingung: restlast(ro) <= rl_ub
        return inputs['rl_ub']-restlast_by_ro(ro, inputs)
    
    def f_constraint_lb(ro, inputs, key):
        # Randbedingung: f1_lb <= f1(ro)
        return results_by_ro(ro, inputs)[key]-inputs[key+'_lb']
    
    def f_constraint_ub(ro, inputs, key):
        # Randbedingung: f1(ro) <= f1_ub
        return inputs[key+'_ub']-results_by_ro(ro, inputs)[key]
    
    def tx_constraint_lb(ro, inputs, key):
        # Randbedingung: tx_lb <= tx(ro)
        return results_by_ro(ro, inputs)[key]-inputs[key+'_lb']
    
    def tx_constraint_ub(ro, inputs, key):
        # Randbedingung: tx(ro) <= tx_ub
        return inputs[key+'_ub']-results_by_ro(ro, inputs)[key]
    
    # Bounds for ro
    ro_lb = inputs['ro_lb']
    ro_ub = inputs['ro_ub']
    bnds = ((ro_lb, ro_ub),) # Grenzwerte zusammenfassen
   
    # Constraints (Nebenbedingungen)
    cons = (
        {'type' : 'ineq', 'fun' : restlast_constraint_lb, 'args': (inputs,)},
        {'type' : 'ineq', 'fun' : restlast_constraint_ub, 'args': (inputs,)},
        {'type' : 'ineq', 'fun' : f_constraint_lb, 'args': (inputs, 'f1',)},
        {'type' : 'ineq', 'fun' : f_constraint_ub, 'args': (inputs, 'f1',)},
        {'type' : 'ineq', 'fun' : f_constraint_lb, 'args': (inputs, 'f2',)},
        {'type' : 'ineq', 'fun' : f_constraint_ub, 'args': (inputs, 'f2',)},
        {'type' : 'ineq', 'fun' : f_constraint_lb, 'args': (inputs, 'f3',)},
        {'type' : 'ineq', 'fun' : f_constraint_ub, 'args': (inputs, 'f3',)},
        {'type' : 'ineq', 'fun' : f_constraint_lb, 'args': (inputs, 'f4',)},
        {'type' : 'ineq', 'fun' : f_constraint_ub, 'args': (inputs, 'f4',)},
        {'type' : 'ineq', 'fun' : tx_constraint_lb, 'args': (inputs, 't14x',)},
        {'type' : 'ineq', 'fun' : tx_constraint_ub, 'args': (inputs, 't14x',)},
        {'type' : 'ineq', 'fun' : tx_constraint_lb, 'args': (inputs, 't23x',)},
        {'type' : 'ineq', 'fun' : tx_constraint_ub, 'args': (inputs, 't23x',)},
        )
    
    initial_guess = ro_ub
    
    res = minimize(lambda x: -x,  # mit x=ro --> Maximiere ro
                   x0=(initial_guess,),
                   method='SLSQP',
                   bounds=bnds,
                   constraints=cons,
                   tol=1e-6,
                   options={'maxiter': 50,
                            'eps': 0.1,
                            'disp': True})
    return res

def scalar_vec_projection(x, y):
    '''
    Project vector x onto y. Returns a scalar value.
    To obtain vector projection multiply scalar projection by a unit vector in 
    the direction of the vector onto which the first vector is projected.

    Parameters
    ----------
    x : array
        vector array.
    y : array
        vector array.

    Returns
    -------
    float
        scalar.
    '''
    return np.dot(x, y) / np.linalg.norm(y)

def xy_load(ml, deg):
    # https://math.stackexchange.com/questions/180874/convert-angle-radians-to-a-heading-vector
    load_vec = np.array([ml*np.cos(np.radians(deg)),
                         ml*np.sin(np.radians(deg)),
                         0.])
    
    mlx = scalar_vec_projection(load_vec, np.array([1., 0., 0.]))
    mly = scalar_vec_projection(load_vec, np.array([0, 1., 0.]))
    return mlx, mly

def vec_load(mlx, mly):
    rad = np.arctan2(mly, mlx)
    mag = np.linalg.norm([mlx, mly])
    return float(mag), rad

def rotate(v, theta):
    '''
    Rotate vector v about angle theta (rad).

    Parameters
    ----------
    v : TYPE
        DESCRIPTION.
    theta : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    v_rot = np.dot(rot, v)
    return v_rot[0], v_rot[1]

def check_liftoffs(results):
        
    liftoffs = [(k, results[k]) for k in ['f1', 'f2', 'f3', 'f4'] if results[k]<=0]
    count = len(liftoffs)
    lift_ids = []
    msg = []
    for stuetze in liftoffs:
        if stuetze[0] == 'f1':
            lift_ids.append(1)
            msg.append('Stütze A/1 hebt ab.')
            
        if stuetze[0] == 'f2':
            lift_ids.append(2)
            msg.append('Stütze B/2 hebt ab.')
            
        if stuetze[0] == 'f3':
            lift_ids.append(3)
            msg.append('Stütze B/2 hebt ab.')
            
        if stuetze[0] == 'f4':
            lift_ids.append(4)
            msg.append('Stütze D/4 hebt ab.')
    
    return count, lift_ids, msg

if __name__ == "__main__":
    # Decompose to x, y
    ml = 100
    deg = 45
    
    print(xy_load(ml, deg))
    
    # Compose from x, y
    mlx = 70.71
    mly = 70.71
    
    ml, rad = vec_load(mlx, mly)
    print(ml, np.degrees(rad))
    
    # Compose from x, y
    mlx = 74552.9
    mly = 129129.3
    
    ml, rad = vec_load(mlx, mly)
    print(ml, np.degrees(rad))