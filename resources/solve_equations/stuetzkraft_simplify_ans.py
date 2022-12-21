# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 12:54:21 2022

@author: 500585
"""
import pickle
from sympy import simplify, symbols

if __name__ == "__main__":
    ans = pickle.load(open("ans_elasto_pickle.p", "rb"))
    
    y1, y2, y3, y4, d1, d2, d3, d4, dc, d23, d14, dt, h = symbols('y1 y2 y3 y4\
    d1 d2 d3 d4 dc d23 d14 dt h')
    
    ans_simpl = {}
    for key in ans:
        expr = ans[key]
        expr = expr.subs([(y1, h),
                          (y2, h),
                          (y3, h),
                          (y4, h),
                          (d1, dc),
                          (d2, dc),
                          (d3, dc),
                          (d4, dc),
                          (d23, dt),
                          (d14, dt)]) 
        
        ans_simpl[key] = simplify(expr)
        print(f'{key}: {ans_simpl[key]}\n---')