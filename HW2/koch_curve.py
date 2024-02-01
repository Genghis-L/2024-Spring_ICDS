#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:30:18 2024

@author: bing
"""

from math import sin, cos, pi
from matplotlib import pyplot as plt


def get_u_coordinates(s, t):
    '''it returns the coordinates (x, y)'''

    u_x = (t[0]-s[0])*cos(pi/3)-(t[1]-s[1])*sin(pi/3)+s[0]
    u_y = (t[0]-s[0])*sin(pi/3)+(t[1]-s[1])*cos(pi/3)+s[1]

    u = (u_x, u_y)

    return u


def get_s_coordinates(p1, p2):
    '''it returns the coordinates (x, y)'''

    s_x = (2*p1[0]+1*p2[0])/3
    s_y = (2*p1[1]+1*p2[1])/3

    s = (s_x, s_y)

    return s


def get_t_coordinates(p1, p2):
    '''it returns the coordinates (x, y)'''

    t_x = (1*p1[0]+2*p2[0])/3
    t_y = (1*p1[1]+2*p2[1])/3

    t = (t_x, t_y)

    return t


def koch_curve(p1, p2, n, n_max):
    '''it returns a list of coordinates (x, y)'''
    if n_max == n:
        return [p1, p2]

    s = get_s_coordinates(p1, p2)
    t = get_t_coordinates(p1, p2)
    u = get_u_coordinates(s, t)

    lst = koch_curve(p1, s, n, n_max-1) + koch_curve(s, u, n, n_max-1)[1:] + \
        koch_curve(u, t, n, n_max-1)[1:] + koch_curve(t, p2, n, n_max-1)[1:]

    return lst


if __name__ == "__main__":
    p1 = (0, 0)
    p2 = (100, 0)
    n_max = 3
    coordinates = koch_curve(p1, p2, 0, n_max)

    # Uncomment the following statements
    # They will plot the koch curve
    x = [c[0] for c in coordinates]
    y = [c[1] for c in coordinates]
    plt.axis('equal')
    plt.plot(x, y)
