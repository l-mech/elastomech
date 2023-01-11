# -*- coding: utf-8 -*-
"""A script to validate the results of the Support Force Distribution Dashboard."""
from model_plain import results_plain
from helpers import check_liftoffs, case_dependent_results
from plot import topview_plot
import loadcases as lc
import plotly.io as pio
pio.renderers.default = 'browser'

loadcases = [
    lc.elast_a(),    # Elastostatisches Modell
    lc.elast_b(),
    lc.elast_c(),
    lc.liftoff_a(),  # Abheben Stütze 1/A
    lc.liftoff_b(),  # Abheben Stütze 2/B
    lc.liftoff_c(),  # Abheben Stütze 3/C
    lc.liftoff_d()   # Abheben Stütze 4/D
]

for (ini, expected) in loadcases:

    # Compute results
    results = results_plain(ini['fl'], ini['mlx'], ini['mly'], ini['fe'], ini['y1'], ini['y2'], ini['y3'], ini['y4'], ini['xe'], ini['x14'], ini['x23'], ini['d14'], ini['d23'], ini['d1'], ini['d2'], ini['d3'], ini['d4'])
    count, lift_ids, msg = check_liftoffs(results)

    print(f'Liftoff: {msg}')

    if count > 0:
        results, errors, warnings = case_dependent_results(ini['fl'], ini['mlx'], ini['mly'], ini['fe'], ini['y1'], ini['y2'], ini['y3'], ini['y4'], ini['xe'], ini['x14'], ini['x23'], ini['d14'], ini['d23'], ini['d1'], ini['d2'], ini['d3'], ini['d4'])
        print(f'Errors: {errors}')
        print(f'Warnings: {warnings}')

    # Plot
    range_x = [-ini['x23'] * 1.5, ini['x23'] * 1.5]
    range_y = [-max(ini['y3'], ini['y4']) * 1.5, max(ini['y1'], ini['y2']) * 1.5]
    data = ini | results
    fig = topview_plot(data, range_x, range_y)
    fig.show()

    # Print results
    print('Abweichungen SOLL-IST:')
    for key in expected:
        soll = expected[key]
        ist = results[key]
        delta = soll - ist
        if soll != 0:
            percent = delta / soll * 100
        else:
            percent = 0.
        print(f'{key}: {delta:.6f} ({percent:.3f}%)')
