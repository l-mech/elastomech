# -*- coding: utf-8 -*-
"""Predefined loadcases and parameter limits for both dashboard pages."""
from helpers import vec_load

# =============================================================================
# ---- Parameter limits
# =============================================================================
lim_support_force_dist = {
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
    'phi_deg_boom_max': 360.,
    'fe_min': 0.,
    'fe_max': 100000.,
    'xe_min': -10.,
    'xe_max': 10.
}

lim_working_radius = {
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
    'phi_deg_boom_max': 360.,
    'fe_min': 0.,
    'fe_max': 100000.,
    'xe_min': -10.,
    'xe_max': 10.,
    # Constraints
    'rl_min': 0.,
    'rl_max': 100000.,
    'ro_min': 1.,
    'ro_max': 30.,
    'f1_min': 0.,
    'f1_max': 100000.,
    'f2_min': 0.,
    'f2_max': 100000.,
    'f3_min': 0.,
    'f3_max': 100000.,
    'f4_min': 0.,
    'f4_max': 100000.,
    'f_ro_min': 0.,
    'f_ro_max': 3000. * 10.,
    't14x_min': -200000.,
    't14x_max': 200000.,
    't23x_min': -200000.,
    't23x_max': 200000.,
    'sv14_min': 0.,
    'sv14_max': 500.0e+6,
    'sv23_min': 0.,
    'sv23_max': 500.0e+6,
    # Frame Box Section
    'B_min': 0.1,
    'B_max': 3.,
    'H_min': 0.1,
    'H_max': 3.,
    'tb_min': 0.001,
    'tb_max': 1.5,
    'th_min': 0.001,
    'th_max': 1.5
}


# =============================================================================
# ---- Predefined loadcases for Support Force Distribution App
# =============================================================================
def elast_a():
    """
    Testcase Elastostatisches Modell.

    - phi = 0°
    - mit Eigengewicht
    """
    ini = {  # Lasten
        'fl': 50000.,
        'mlx': 0.,
        'mly': 56755.1197626084,
        'fe': 3000.,
        'xe': 3.2,
        'h': 3.,
        'x14': 4.805,
        'x23': 0.78,
        'd14': 30230369.9624028,
        'd23': 155189025.287762,
        'd': 3001412.83555556,
        'phi_deg_boom': 0.
    }

    ini['ml'], _ = vec_load(ini['mlx'], ini['mly'])

    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    # Boom angle
    ini['phi_deg_load'] = ini['phi_deg_boom'] + 90.
    # d
    ini['d1'] = ini['d']
    ini['d2'] = ini['d']
    ini['d3'] = ini['d']
    ini['d4'] = ini['d']

    expected = {
        'f1': 9641.46103514847,
        'f2': 16858.5389648515,
        'f3': 16858.5389648515,
        'f4': 9641.46103514847,
        's1': 0.00321230752428759,
        's2': 0.00561686775146047,
        's3': 0.00561686775146047,
        's4': 0.00321230752428759,
        't14x': 0.,
        't23x': 0.,
    }

    return ini, expected


def elast_b():
    """
    Testcase Elastostatisches Modell.

    - phi = 30°
    - mit Eigengewicht
    """
    ini = {  # Lasten
        'fl': 50000.,
        'mlx': -62619.2469377536,
        'mly': 108459.717227891,
        'fe': 3000.,
        'xe': 3.2,
        'h': 3.,
        'x14': 4.805,
        'x23': 0.78,
        'd14': 30230369.9624028,
        'd23': 155189025.287762,
        'd': 3001412.83555556,
        'phi_deg_boom': 30.,
    }

    ini['ml'], _ = vec_load(ini['mlx'], ini['mly'])

    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    # Boom angle
    ini['phi_deg_load'] = ini['phi_deg_boom'] + 90.
    # d
    ini['d1'] = ini['d']
    ini['d2'] = ini['d']
    ini['d3'] = ini['d']
    ini['d4'] = ini['d']

    expected = {
        'f1': 17672.7419752557,
        'f2': 19263.7991810366,
        'f3': 5195.5173403795,
        'f4': 10867.9415033282,
        's1': 0.0058881410000982,
        's2': 0.00641824375268619,
        's3': 0.00173102389609053,
        's4': 0.0036209419026212,
        't14x': 20414.4014157823,
        't23x': -42204.8455219713,
    }

    return ini, expected


def elast_c():
    """
    Testcase Elastostatisches Modell.

    - phi = 333°
    - mit Eigengewicht
    """
    ini = {  # Lasten
        'fl': 50000.,
        'mlx': 56857.0864211697,
        'mly': 111588.315122602,
        'fe': 3000.,
        'xe': 3.2,
        'h': 3.,
        'x14': 4.805,
        'x23': 0.78,
        'd14': 30230369.9624028,
        'd23': 155189025.287762,
        'd': 3001412.83555556,
        'phi_deg_boom': 333.,
    }

    ini['ml'], _ = vec_load(ini['mlx'], ini['mly'])

    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    # Boom angle
    ini['phi_deg_load'] = ini['phi_deg_boom'] + 90.
    # d
    ini['d1'] = ini['d']
    ini['d2'] = ini['d']
    ini['d3'] = ini['d']
    ini['d4'] = ini['d']

    expected = {
        'f1': 11461.1163094514,
        'f2': 5562.70262035366,
        'f3': 18336.4352269871,
        'f4': 17639.7458432079,
        's1': 0.00381857376422192,
        's2': 0.00185336137516851,
        's3': 0.0061092679453385,
        's4': 0.00587714746676719,
        't14x': -18535.8886012695,
        't23x': 38321.1978199003,
    }

    return ini, expected


def liftoff_a():
    """
    Testcase Abheben Stütze 1/A.

    - phi = 270°
    - Ausladung 10m
    - FKorb 406kg
    - Feigen 3000 N
    - mit Eigengewicht
    """
    ini = {  # Lasten
        'fl': 50000.,
        'mlx': 125238.493875507,
        'mly': -2.30153620899991E-11,
        'fe': 3000.,
        'xe': 3.2,
        'h': 3.,
        'x14': 4.805,
        'x23': 0.78,
        'd14': 30230369.9624028,
        'd23': 155189025.287762,
        'd': 3001412.83555556,
        'phi_deg_boom': 270.,
    }

    ini['ml'], _ = vec_load(ini['mlx'], ini['mly'])

    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    # Boom angle
    ini['phi_deg_load'] = ini['phi_deg_boom'] + 90.
    # d
    ini['d1'] = ini['d']
    ini['d2'] = ini['d']
    ini['d3'] = ini['d']
    ini['d4'] = ini['d']

    expected = {
        'f1': 0,
        'f2': 5626.91768741545,
        'f3': 38252.2228676427,
        'f4': 9120.85944494181,
        's1': -0.0061844450513257,
        's2': 0.0018747563216754,
        's3': 0.0127447388824678,
        's4': 0.00303885534735296,
        't14x': -27362.5783348254,
        't23x': 97875.9155406819,
    }

    return ini, expected


def liftoff_b():
    """
    Testcase Abheben Stütze 2/B.

    - phi = 320°
    - Ausladung 12m
    - FKorb 406kg
    - Feigen 5000 N
    - mit Eigengewicht
    """
    ini = {  # Lasten
        'fl': 50000.,
        'mlx': 109848.595018512,
        'mly': 130912.457754739,
        'fe': 5000.,
        'xe': 3.2,
        'h': 3.,
        'x14': 4.805,
        'x23': 0.78,
        'd14': 30230369.9624028,
        'd23': 155189025.287762,
        'd': 3001412.83555556,
        'phi_deg_boom': 320.,
    }

    ini['ml'], _ = vec_load(ini['mlx'], ini['mly'])

    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    # Boom angle
    ini['phi_deg_load'] = ini['phi_deg_boom'] + 90.
    # d
    ini['d1'] = ini['d']
    ini['d2'] = ini['d']
    ini['d3'] = ini['d']
    ini['d4'] = ini['d']

    expected = {
        'f1': 9191.90083024792,
        'f2': 0,
        'f3': 21013.8840188472,
        'f4': 24794.2151509049,
        't14x': -46806.942961971,
        't23x': 63041.6520565415,
        's1': 0.00306252466217181,
        's2': -0.00504969323594799,
        's3': 0.00700133076326954,
        's4': 0.00826084797705463,
    }

    return ini, expected


def liftoff_c():
    """
    Testcase Abheben Stütze 3/C.

    - phi = 45°
    - Ausladung 12m
    - FKorb 406kg
    - Feigen 5000 N
    - mit Eigengewicht
    """
    ini = {  # Lasten
        'fl': 50000.,
        'mlx': -120840.360440805,
        'mly': 120840.360440805,
        'fe': 5000.,
        'xe': 3.2,
        'h': 3.,
        'x14': 4.805,
        'x23': 0.78,
        'd14': 30230369.9624028,
        'd23': 155189025.287762,
        'd': 3001412.83555556,
        'phi_deg_boom': 45.,
    }

    ini['ml'], _ = vec_load(ini['mlx'], ini['mly'])

    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    # Boom angle
    ini['phi_deg_load'] = ini['phi_deg_boom'] + 90.
    # d
    ini['d1'] = ini['d']
    ini['d2'] = ini['d']
    ini['d3'] = ini['d']
    ini['d4'] = ini['d']

    expected = {
        'f1': 24822.756660899,
        'f2': 22817.3034125685,
        'f3': 0,
        'f4': 7359.93992653249,
        't14x': 52388.4502030997,
        't23x': -68451.9102377054,
        's1': 0.00827035733533284,
        's2': 0.00760218759054685,
        's3': -0.00596733238948251,
        's4': 0.00245215847661629,
    }

    return ini, expected


def liftoff_d():
    """
    Testcase Abheben Stütze 4/D.

    - phi = 120°
    - Ausladung 8m
    - FKorb 406kg
    - Feigen 5000 N
    - mit Eigengewicht
    """
    ini = {  # Lasten
        'fl': 50000.,
        'mlx': -68920.8227487951,
        'mly': -39791.4555667873,
        'fe': 5000.,
        'xe': 3.2,
        'h': 3.,
        'x14': 4.805,
        'x23': 0.78,
        'd14': 30230369.9624028,
        'd23': 155189025.287762,
        'd': 3001412.83555556,
        'phi_deg_boom': 120.,
    }

    ini['ml'], _ = vec_load(ini['mlx'], ini['mly'])

    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    # Boom angle
    ini['phi_deg_load'] = ini['phi_deg_boom'] + 90.
    # d
    ini['d1'] = ini['d']
    ini['d2'] = ini['d']
    ini['d3'] = ini['d']
    ini['d4'] = ini['d']

    expected = {
        'f1': 3421.40455384291,
        'f2': 35565.3992376229,
        'f3': 16013.1962085341,
        'f4': 0,
        't14x': 10264.2136615287,
        't23x': -58656.6090872664,
        's1': 0.00113993133943855,
        's2': 0.011849552589469,
        's3': 0.00533521947358839,
        's4': -0.0056050154711532,
    }

    return ini, expected

# =============================================================================
# ---- Predefined loadcases for Working Radius App
# =============================================================================


def ro_default():
    """
    Testcase Abheben Stütze 1/A.

    - phi = 270°
    - Ausladung 10m
    - FKorb 406kg
    - Feigen 3000 N
    - mit Eigengewicht
    """
    ini = {  # Lasten
        'fl': 50000.,
        'mlx': 125238.493875507,
        'mly': -2.30153620899991E-11,
        'fe': 5000.,
        'xe': 3.2,
        'h': 3.,
        'x14': 4.805,
        'x23': 0.78,
        'd14': 30230369.9624028,
        'd23': 155189025.287762,
        'd': 3001412.83555556,
        'phi_deg_boom': 270.,
        'f_ro': 406. * 9.81,
        'H': 0.410,
        'B': 0.800,
        'th': 0.007,
        'tb': 0.014,
    }

    ini['ml'], _ = vec_load(ini['mlx'], ini['mly'])

    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    # Boom angle
    ini['phi_deg_load'] = ini['phi_deg_boom'] + 90.
    # d
    ini['d1'] = ini['d']
    ini['d2'] = ini['d']
    ini['d3'] = ini['d']
    ini['d4'] = ini['d']

    expected = {
        'f1': 0,
        'f2': 5626.91768741545,
        'f3': 38252.2228676427,
        'f4': 9120.85944494181,
        's1': -0.0061844450513257,
        's2': 0.0018747563216754,
        's3': 0.0127447388824678,
        's4': 0.00303885534735296,
        't14x': -27362.5783348254,
        't23x': 97875.9155406819,
    }

    return ini, expected


def ro_pillow_a():
    """
    Testcase Kissenform.

    Normiert@
    - phi = 0°
    - Ausladung 30m
    - FKorb 2542kg --> ml 748250.3Nm
    - Feigen 5000N
    """
    ini = {  # Lasten
        'fl': 50000.,
        'mlx': 125238.493875507,
        'mly': -2.30153620899991E-11,
        'fe': 5000.,
        'xe': 3.2,
        'h': 3.,
        'x14': 4.805,
        'x23': 0.78,
        'd14': 30230369.9624028,
        'd23': 155189025.287762,
        'd': 3001412.83555556,
        'phi_deg_boom': 270.,
        'f_ro': 2542. * 9.81,
        'H': 0.410,
        'B': 0.800,
        'th': 0.007,
        'tb': 0.014,
    }

    ini['ml'], _ = vec_load(ini['mlx'], ini['mly'])

    # Symmetrie
    ini['y1'] = ini['h']
    ini['y2'] = ini['h']
    ini['y3'] = ini['h']
    ini['y4'] = ini['h']
    # Boom angle
    ini['phi_deg_load'] = ini['phi_deg_boom'] + 90.
    # d
    ini['d1'] = ini['d']
    ini['d2'] = ini['d']
    ini['d3'] = ini['d']
    ini['d4'] = ini['d']

    expected = {

    }

    return ini, expected
