#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 09:42:33 2022

@author: bing
"""

# Q1
def AND(bit1, bit2):
    if bit1 == '1' and bit2 == '1':
        return '1'
    else:
        return '0'


def OR(bit1, bit2):
    if bit1 == '0' and bit2 == '0':
        return '0'
    else:
        return '1'


def XOR(bit1, bit2):
    if bit1 == bit2:
        return '0'
    else:
        return '1'


# Q2
def half_adder(bit1, bit2):
    return XOR(bit1, bit2), AND(bit1, bit2)


def full_adder(bit1, bit2, c_in):
    a_xor_b = XOR(bit1, bit2)
    s = XOR(a_xor_b, c_in)
    c_out = OR(AND(c_in, bit2), AND(bit1, bit2))

    return s, c_out


# Q3
def add(bin_str1, bin_str2):
    len_1, len_2 = len(bin_str1), len(bin_str2)
    if len_1 > len_2:
        difference = len_1 - len_2
        bin_str2 = ''.join(['0'*difference, bin_str2])
    else:
        difference = len_2 - len_1
        bin_str1 = ''.join(['0'*difference, bin_str1])

    s, c_out = half_adder(bin_str1[-1], bin_str2[-1])

    for i in range(len(bin_str1)-2, -1, -1):
        s_temp, c_out = full_adder(bin_str1[i], bin_str2[i], c_out)

        s = s_temp + s
        pass

    if c_out != '0':
        s = c_out+s

    return s
        

##Tests
if __name__=="__main__":
    
    str1 = '10'
    str2 = '10'
    print(add(str1, str2))
    
    