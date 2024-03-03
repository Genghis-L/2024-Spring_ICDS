#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 00:26:06 2024

@author: kehanluo
"""

import matplotlib.pyplot as plt
from matplotlib.pyplot import legend, plot, xlim, ylim, title, xlabel, ylabel
from math import sin, pi


x = [i*0.1 for i in range(-100, 100)]
y = [sin(v) for v in x]

plot(x, y, "c*", label='f(x)')
legend()

xlim(-pi, pi)
ylim(-2, 2)

xlabel('x')
ylabel('sin(x)')
title('f(x) = sin(x)')

