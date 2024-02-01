#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 23:48:42 2021

@author: bing
"""


def fraction2binary(f, space):
    # complete the code

    b = ''
    while f != 0:
        f *= 2
        if f >= 1:
            b += '1'
            f -= 1
        else:
            b += '0'
    b = b[0:space]
    return '0.'+b


def binary2fraction(b):
    # complete the code
    
    b_lst = b.split('.')
    dec_fraction = 0
    l1 = len(b_lst[1])
    for i in range(l1):
        dec_fraction += int(b_lst[1][i])*2**(-i-1)

    dec_integer = 0
    l2 = len(b_lst[0])
    for i in range(l2):
        dec_integer += int(b_lst[0][i])*2**(l2-i)

    return dec_fraction+dec_integer


if __name__ == '__main__':
    print('2.07 - 2 =', 2.07 - 2)
    f = 0.07
    l = 52
    print('The binary of 0.07 in your machine:')
    print(fraction2binary(f, l))
    print('Influence of the Truncation error')
    print(binary2fraction(fraction2binary(f, l)))
