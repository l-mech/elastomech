# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:05:53 2022

@author: 500585
"""
import numpy as np

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
    return mag, rad

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