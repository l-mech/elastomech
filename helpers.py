# -*- coding: utf-8 -*-
"""Collection of helper functions for both dashboards."""
import numpy as np
from model_plain import results_plain, results_liftoff_plain
from scipy.optimize import minimize


def cart2pol(x, y):
    """
    Convert coordinates from cartesian (x, y) to polar (rho, phi).

    Parameters
    ----------
    x : number/array
        Cartesian x.
    y : number/array
        Cartesian y.

    Returns
    -------
    rho : number/array
        Polar radius.
    phi : number/array
        Polar angle in radians.

    """
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho, phi):
    """
    Convert coordinates from polar (rho, phi) to cartesian (x, y).

    Parameters
    ----------
    rho : number/array
        Polar radius.
    phi : number/array
        Polar angle in radians.

    Returns
    -------
    x : number/array
        Cartesian x.
    y : number/array
        Cartesian y.

    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def case_dependent_results(fl, mlx, mly, fe, y1, y2, y3, y4, xe, x14, x23, d14, d23, d1, d2, d3, d4, x1=None, x3=None):
    """
    Check if one or more supports are lifting off ground and select the appropriate calculation model. Return the results of the calculation.

    If there is no lift-off of any support, the results are calculated from the (statically overdetermined) elastostatic model.
    If exactly one support lifts off, the corresponding statically determined model is used.
    If several supports lift off, the solution of the elastostatic model is returned and an error string is generated.

    Parameters
    ----------
    fl : float
    mlx : float
    mly : float
    fe : float
    y1 : float
    y2 : float
    y3 : float
    y4 : float
    xe : float
    x14 : float
    x23 : float
    d14 : float
    d23 : float
    d1 : float
    d2 : float
    d3 : float
    d4 : float
    x1 : float, optional
         The default is None.
    x3 : float, optional
         The default is None.

    Returns
    -------
    results : dict
        Dict of results.
    errors : list of strings
        List of error messages.
    warnings : list of strings
        List of warning messages.
    """
    # Initial run
    errors = []
    warnings = []
    results = results_plain(fl, mlx, mly, fe, y1, y2, y3, y4, xe, x14, x23, d14, d23, d1, d2, d3, d4, x1, x3)

    # Check if elastostatic model is valid
    # if any(f < 0 for f in [results['f1'], results['f2'], results['f3'], results['f4']]):
    count, lift_ids, _ = check_liftoffs(results)

    if count == 1:  # Genau eine Stütze hebt ab
        results = results_liftoff_plain(fl, mlx, mly, fe, y1, y2, y3, y4, xe, x14, x23, d14, d23, d1, d2, d3, d4, lift=lift_ids[0], x1=x1, x3=x3)
        count, lift_ids, warnings = check_liftoffs(results)

    if count > 1:  # Mehrere Stützen heben ab
        errors = ['Mehr als eine Stütze hebt ab. Berechnung ungültig.']

    return results, errors, warnings


def load_moment(force_distance_pairs):
    """
    Return load moment from multiple pairs of forces and distances.

    Parameters
    ----------
    force_distance_pairs : list of tuples
        List of force-distance pairs in the form [(f1, d1), (f2, d2)].

    Returns
    -------
    ml : float
        Resulting load moment.
    """
    mls = []
    for (f, r) in force_distance_pairs:
        mls.append(f * r)
    ml = sum(mls)
    return ml


def restlast(results):
    """
    Return remaining load of the four tilting edges.

    Parameters
    ----------
    results : dict
        Result dict.

    Returns
    -------
    rl_min : tuple
        Minimal remaining load in the form of (key, value).
    rl : dict
        Remaining loads of the four tilting edges.
    """
    f1, f2, f3, f4 = results['f1'], results['f2'], results['f3'], results['f4']
    f12 = f1 + f2
    f23 = f2 + f3
    f34 = f3 + f4
    f14 = f1 + f4
    ks = ['f12', 'f23', 'f34', 'f14']
    vls = [f12, f23, f34, f14]
    minpos = vls.index(min(vls))
    rl_min = (ks[minpos], vls[minpos])
    rl = {'f12': f12, 'f23': f23, 'f34': f34, 'f14': f14}
    return rl_min, rl


def limited_reachout(inputs):
    """
    Maximize working radius ro within its boundaries (ro_lb, ro_ub).

    Additional constraints for remaining load, supporting forces, torsional mom
    ents and equivalent stresses are also taken into account. Constraints are a
    lways active, i.e. the corresponding boundaries lb and ub must be specified
    in a range that they have no influence.

    SLSQP method ([Sequential Least Squares Programming](https://docs.scipy.org
    /doc/scipy/reference/optimize.minimize-slsqp.html#optimize-minimize-slsqp))
    is used for optimization

    Parameters
    ----------
    inputs : dict
        Dict of input values.

    Returns
    -------
    res: OptimizeResult
        The optimization result represented as a OptimizeResult object. Importa
        nt attributes are: x the solution array, success a Boolean flag indicat
        ing if the optimizer exited successfully and message which describes th
        e cause of the termination.
    """
    def results_by_ro(ro, inputs):
        i = inputs
        ml = load_moment([(i['f_ro'], ro)])
        mlx, mly = xy_load(ml, i['phi_deg_load'])
        results, _, _ = case_dependent_results(i['fl'], mlx, mly, i['fe'], i['y1'], i['y2'], i['y3'], i['y4'], i['xe'], i['x14'], i['x23'], i['d14'], i['d23'], i['d1'], i['d2'], i['d3'], i['d4'], x1=i['x1'], x3=i['x3'])

        # Zusätzlich Spannungen im Rahmen berechnen
        results['sv14'] = box_section_stress(B=i['B'], H=i['H'], tb=i['tb'], th=i['th'], m_t=results['t14x'], m_by=results['t14y'])
        results['sv23'] = box_section_stress(B=i['B'], H=i['H'], tb=i['tb'], th=i['th'], m_t=results['t23x'], m_by=results['t23y'])

        return results

    def restlast_by_ro(ro, inputs):
        results = results_by_ro(ro, inputs)
        _, rl = restlast(results)
        return rl

    def restlast_constraint_lb(ro, inputs, key):
        # Randbedingung: rl_lb <= restlast(ro)
        return restlast_by_ro(ro, inputs)[key] - inputs['rl_lb']

    def restlast_constraint_ub(ro, inputs, key):
        # Randbedingung: restlast(ro) <= rl_ub
        return inputs['rl_ub'] - restlast_by_ro(ro, inputs)[key]

    def f_constraint_lb(ro, inputs, key):
        # Randbedingung: f1_lb <= f1(ro)
        return results_by_ro(ro, inputs)[key] - inputs[key + '_lb']

    def f_constraint_ub(ro, inputs, key):
        # Randbedingung: f1(ro) <= f1_ub
        return inputs[key + '_ub'] - results_by_ro(ro, inputs)[key]

    def tx_constraint_lb(ro, inputs, key):
        # Randbedingung: tx_lb <= tx(ro)
        return results_by_ro(ro, inputs)[key] - inputs[key + '_lb']

    def tx_constraint_ub(ro, inputs, key):
        # Randbedingung: tx(ro) <= tx_ub
        return inputs[key + '_ub'] - results_by_ro(ro, inputs)[key]

    def stress_constraint_lb(ro, inputs, key):
        # Randbedingung: sv_lb <= sv(ro)
        return results_by_ro(ro, inputs)[key] - inputs[key + '_lb']

    def stress_constraint_ub(ro, inputs, key):
        # Randbedingung: sv(ro) <= sv_ub
        return inputs[key + '_ub'] - results_by_ro(ro, inputs)[key]

    # Bounds for ro
    ro_lb = inputs['ro_lb']
    ro_ub = inputs['ro_ub']
    bnds = ((ro_lb, ro_ub),)  # Grenzwerte zusammenfassen

    # Constraints (Nebenbedingungen)
    cons = (
        {'type': 'ineq', 'fun': restlast_constraint_lb, 'args': (inputs, 'f12')},
        {'type': 'ineq', 'fun': restlast_constraint_ub, 'args': (inputs, 'f12')},
        {'type': 'ineq', 'fun': restlast_constraint_lb, 'args': (inputs, 'f23')},
        {'type': 'ineq', 'fun': restlast_constraint_ub, 'args': (inputs, 'f23')},
        {'type': 'ineq', 'fun': restlast_constraint_lb, 'args': (inputs, 'f34')},
        {'type': 'ineq', 'fun': restlast_constraint_ub, 'args': (inputs, 'f34')},
        {'type': 'ineq', 'fun': restlast_constraint_lb, 'args': (inputs, 'f14')},
        {'type': 'ineq', 'fun': restlast_constraint_ub, 'args': (inputs, 'f14')},
        {'type': 'ineq', 'fun': f_constraint_lb, 'args': (inputs, 'f1',)},
        {'type': 'ineq', 'fun': f_constraint_ub, 'args': (inputs, 'f1',)},
        {'type': 'ineq', 'fun': f_constraint_lb, 'args': (inputs, 'f2',)},
        {'type': 'ineq', 'fun': f_constraint_ub, 'args': (inputs, 'f2',)},
        {'type': 'ineq', 'fun': f_constraint_lb, 'args': (inputs, 'f3',)},
        {'type': 'ineq', 'fun': f_constraint_ub, 'args': (inputs, 'f3',)},
        {'type': 'ineq', 'fun': f_constraint_lb, 'args': (inputs, 'f4',)},
        {'type': 'ineq', 'fun': f_constraint_ub, 'args': (inputs, 'f4',)},
        {'type': 'ineq', 'fun': tx_constraint_lb, 'args': (inputs, 't14x',)},
        {'type': 'ineq', 'fun': tx_constraint_ub, 'args': (inputs, 't14x',)},
        {'type': 'ineq', 'fun': tx_constraint_lb, 'args': (inputs, 't23x',)},
        {'type': 'ineq', 'fun': tx_constraint_ub, 'args': (inputs, 't23x',)},
        {'type': 'ineq', 'fun': stress_constraint_lb, 'args': (inputs, 'sv14',)},
        {'type': 'ineq', 'fun': stress_constraint_ub, 'args': (inputs, 'sv14',)},
        {'type': 'ineq', 'fun': stress_constraint_lb, 'args': (inputs, 'sv23',)},
        {'type': 'ineq', 'fun': stress_constraint_ub, 'args': (inputs, 'sv23',)},
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
    """
    Project vector x onto y. Return a scalar value.

    To obtain vector projection multiply scalar projection by a unit vector in
    the direction of the vector onto which the first vector is projected.

    Parameters
    ----------
    x : array
        Vector array.
    y : array
        Vector array.

    Returns
    -------
    float
        Scalar.
    """
    return np.dot(x, y) / np.linalg.norm(y)


def xy_load(ml, deg):
    """
    Return components of a (load) vector defined by its magnitude and angle.

    Parameters
    ----------
    ml : float
        vector magnitude.
    deg : float
        angle in degrees.

    Returns
    -------
    mlx : float
        Vector x-component.
    mly : float
        Vector y-component.
    """
    # https://math.stackexchange.com/questions/180874/convert-angle-radians-to-a-heading-vector
    load_vec = np.array([ml * np.cos(np.radians(deg)),
                         ml * np.sin(np.radians(deg)),
                         0.],
                        dtype=object)

    mlx = scalar_vec_projection(load_vec, np.array([1., 0., 0.]))
    mly = scalar_vec_projection(load_vec, np.array([0, 1., 0.]))
    return mlx, mly


def vec_load(mlx, mly):
    """
    Return magnitude and angle of a given (load) vector.

    Parameters
    ----------
    mlx : number/array
        Vector x-component.
    mly : number/array
        Vector y-component.

    Returns
    -------
    mag: float
        Vector magnitude.
    rad : float
        Angle in radians.
    """
    rad = np.arctan2(mly, mlx)
    mag = np.linalg.norm([mlx, mly])
    return float(mag), rad


def rotate(v, theta):
    """
    Rotate vector v about angle theta (rad).

    Parameters
    ----------
    v : array
        Vector array.
    theta : float
        Angle in radians.

    Returns
    -------
    v_rot[0]: float
        First component of rotated vector.
    v_rot[1]: float
        Second component of rotated vector.
    """
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    v_rot = np.dot(rot, v)
    return v_rot[0], v_rot[1]


def check_liftoffs(results):
    """
    Check if supports lift off of ground and return the number and ids of liftoff supports and a correspondig message.

    Parameters
    ----------
    results : dict
        Dict of results.

    Returns
    -------
    count : int
        Number of liftoff supports.
    lift_ids : list of int
        List of liftoff support ids.
    msg : list of str
        List of message strings.
    """
    liftoffs = [(k, results[k]) for k in ['f1', 'f2', 'f3', 'f4'] if results[k] <= 0]
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


def combined_stress(wt, ia, a_max, m_t, m_b):
    r"""
    Return superposed stress values for torsion + bending.

    All input values must refer to the same location of the cross section, so
    that superposition is valid.

    Parameters
    ----------
    wt : float
        Torsional resistance moment.
    ia : float
        2nd moment of area.
    a_max : float
        Distance from the neutral axis to the fibre.
    m_t : float
        Torsional load.
    m_b : float
        Bending load.

    Returns
    -------
    eq_stress : float
        Equivalent stress using shape modification hypothesis $\sqrt(\sigma_B^2+3\tau^2)$.
    bending_stress : float
        Bending stress using $M_B/I\cdot a_{max}$.
    torsion_stress : float
        Torsional stress using $M_T/W_T$.
    """
    bending_stress = m_b / ia * a_max
    torsion_stress = m_t / wt
    eq_stress = np.sqrt(bending_stress**2 + 3 * torsion_stress**2)
    return eq_stress, bending_stress, torsion_stress


def torsional_resistance_moment_box_section(B, H, tb, th):
    """
    Return the torsional resistance moments of a box section with width B, height H and corresponding wall thicknesses tb and th.

    See Roloff-Matek Tabellenbuch TB 1-14.

    Parameters
    ----------
    B : float
        Outer width of box.
    H : float
        Outer height of box.
    tb : float
        Wall thickness left/right side of box.
    th : float
        Wall thickness top/bottom of box.

    Returns
    -------
    wt_h : float
        Torsional resistance moment of box section $W_{T,h}$ (top and bottom)
    wt_b : float
        Torsional resistance moment of box section $W_{T,b}$ (left and right)
    """
    wt_b = 2 * (B - tb) * (H - th) * tb
    wt_h = 2 * (B - tb) * (H - th) * th
    return wt_h, wt_b


def second_moment_of_area_box_section(B, H, tb, th):
    """
    Return the 2nd moments of area of a box section with width B, height H and corresponding wall thicknesses tb and th.

    Parameters
    ----------
    B : float
        Outer width of box.
    H : float
        Outer height of box.
    tb : float
        Wall thickness left/right side of box.
    th : float
        Wall thickness top/bottom of box.

    Returns
    -------
    iy : float
        2nd moment of area for bending around y-axis (H**3).
    iz : float
        2nd moment of area for bending around z-axis (B**3).
    """
    iz = 1 / 12. * (B**3 * H - (B - 2 * tb)**3 * (H - 2 * th))
    iy = 1 / 12. * (B * H**3 - (B - 2 * tb) * (H - 2 * th)**3)
    return iy, iz


def box_section_stress(B, H, tb, th, m_t, m_by):
    """
    Return equivalent stress for the top/bottom fibre of a box section profile as well as the left/right fibres.

    Convention: The z-axis is perpendicular to the top/bottom, the y-axis is
    perpendicular to the side wall of the box section. Both axes represent the
    neutral fiber of the cross section.

    Parameters
    ----------
    B : float
        Outer width of box.
    H : float
        Outer height of box.
    tb : float
        Wall thickness left/right side of box.
    th : float
        Wall thickness top/bottom of box.
    m_t : float
        Torsional load.
    m_by : float, optional
        Bending load for y-axis.

    Returns
    -------
    eq_stress_h : float
        Equivalent stress for the top/bottom fibre.
    eq_stress_b : float
        Equivalent stress for the side wall fibre.
    """
    iy, iz = second_moment_of_area_box_section(B, H, tb, th)
    wt_h, wt_b = torsional_resistance_moment_box_section(B, H, tb, th)

    eq_stress_h, _, _ = combined_stress(wt=wt_h, ia=iy, a_max=H / 2, m_t=m_t, m_b=m_by)

    return eq_stress_h


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
