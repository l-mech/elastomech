#!/usr/bin/env python
# coding: utf-8

from sympy import Eq, solve, symbols

def solve_elasto_model():
    # Known
    fl, mlx, mly, fe, y1, y2, y3, y4, xe, x1, x2, x3, x14, x23, d14, d23, d1, d2, d3, d4 = symbols('fl, mlx, mly, fe, y1, y2, y3, y4, xe, x1, x2, x3, x14, x23, d14, d23, d1, d2, d3, d4')
    
    # Unknown
    f1, f2, f3, f4, t14x, t23x, t14y, t23y, s1, s2, s3, s4, phi1, phi2, phi3, fry, ffy = symbols('f1, f2, f3, f4, t14x, t23x, t14y, t23y, s1, s2, s3, s4, phi1, phi2, phi3, fry, ffy')
    
    # Rigid Body I
    eq1 = Eq(f3+f2+fry, 0)
    eq2 = Eq(f2*y2-f3*y3+t23x, 0)
    eq3 = Eq((f2+f3)*x1+t23y, 0)
    
    # Rigid Body II
    eq4 = Eq(-fry+ffy-fl-fe, 0)
    eq5 = Eq(t14x+mlx-t23x, 0)
    eq6 = Eq(mly+t14y-t23y-fry*(x23-x1)-ffy*(x14-x3)+fe*xe, 0)
    
    # Rigid Body III
    eq7 = Eq(f1+f4-ffy, 0)
    eq8 = Eq(f1*y1-f4*y4-t14x, 0)
    eq9 = Eq(-t14y-(f1+f4)*x3, 0)
    
    # Compression Springs
    eq10 = Eq(d1*s1-f1, 0)
    eq11 = Eq(d4*s4-f4, 0)
    eq12 = Eq(d2*s2-f2, 0)
    eq13 = Eq(d3*s3-f3, 0)
    
    # Torsion Springs
    eq14 = Eq((phi1-phi2)*d23-t23x, 0)
    eq15 = Eq((phi2-phi3)*d14-t14x, 0)
    
    # Kinematic constraints
    eq16 = Eq((s2-s3)/(y2+y3)-phi1, 0)
    eq17 = Eq((s1-s4)/(y1+y4)-phi3, 0)
    
   
    eqs = [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, eq11, eq12, eq13, eq14, eq15, eq16, eq17]
    unknowns = [f1, f2, f3, f4, t14x, t23x, t14y, t23y, s1, s2, s3, s4, phi1, phi2, phi3, fry, ffy]
    
    print(f'No of equations: {len(eqs)}\nNo of unknowns: {len(unknowns)}')
    
    ans = solve(eqs, unknowns)
    
    return ans

def solve_liftoff_model():
    # Known
    fl, mlx, mly, fe, y1, y2, y3, y4, xe, x1, x2, x3, x14, x23, d14, d23, d1, d2, d3, d4 = symbols('fl, mlx, mly, fe, y1, y2, y3, y4, xe, x1, x2, x3, x14, x23, d14, d23, d1, d2, d3, d4')
    
    # Unknown
    f1, f2, f3, f4, t14x, t23x, t14y, t23y, s1, s2, s3, s4, phi1, phi2, phi3, fry, ffy = symbols('f1, f2, f3, f4, t14x, t23x, t14y, t23y, s1, s2, s3, s4, phi1, phi2, phi3, fry, ffy')
    
    # Liftoff
    f4 = 0
    
    # Rigid Body I
    eq1 = Eq(f3+f2+fry, 0)
    eq2 = Eq(f2*y2-f3*y3+t23x, 0)
    eq3 = Eq((f2+f3)*x1+t23y, 0)
    
    # Rigid Body II
    eq4 = Eq(-fry+ffy-fl-fe, 0)
    eq5 = Eq(t14x+mlx-t23x, 0)
    eq6 = Eq(mly+t14y-t23y-fry*(x23-x1)-ffy*(x14-x3)+fe*xe, 0)
    
    # Rigid Body III
    eq7 = Eq(f1+f4-ffy, 0)
    eq8 = Eq(f1*y1-f4*y4-t14x, 0)
    eq9 = Eq(-t14y-(f1+f4)*x3, 0)
    
    # Compression Springs
    eq10 = Eq(d1*s1-f1, 0)
    eq11 = Eq(d4*s4-f4, 0)
    eq12 = Eq(d2*s2-f2, 0)
    eq13 = Eq(d3*s3-f3, 0)
    
    # Torsion Springs
    eq14 = Eq((phi1-phi2)*d23-t23x, 0)
    eq15 = Eq((phi2-phi3)*d14-t14x, 0)
    
    # Kinematic constraints
    eq16 = Eq((s2-s3)/(y2+y3)-phi1, 0)
    eq17 = Eq((s1-s4)/(y1+y4)-phi3, 0)
    
   
    eqs = [eq1,
           eq2,
           eq3,
           eq4,
           eq5,
           eq6,
           eq7,
           eq8,
           eq9,
           eq10,
           #eq11,
           eq12,
           eq13,
           eq14,
           eq15,
           eq16,
           eq17]
    unknowns = [f1, f2, f3, f4, t14x, t23x, t14y, t23y, s1, s2, s3, s4, phi1, phi2, phi3, fry, ffy]
    
    print(f'No of equations: {len(eqs)}\nNo of unknowns: {len(unknowns)}')
    
    ans = solve(eqs, unknowns)
    return ans  
 
if __name__ == "__main__":
    import pickle
    
    #ans_elasto = solve_elasto_model()
    #pickle.dump(ans_elasto, open( "ans_elasto_pickle.p", "wb" ))
    
    ans_lift = solve_liftoff_model()
    
    # print('Elastostatic model')
    # for key in ans_elasto:
    #     print(f'{key} = {ans_elasto[key]}')
    
    print('Liftoff model')
    for key in ans_lift:
        print(f'{key} = {ans_lift[key]}')
