#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:09:16 2020

@author: xg7
"""


def int_to_hexa(int_code):
    # modified the following to the tests
    dict_int2hex = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5",
                    6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B",
                    12: "C", 13: "D", 14: "E", 15: "F"}
    result = ""
    while int_code:
        result += dict_int2hex[int_code % 16]
        int_code //= 16
    return result[::-1]


## ---test of your code, don't change the followings---##
if __name__ == "__main__":
    int_code = 12
    hexadecimal_code = int_to_hexa(int_code)
    print(int_code, 'converts to', hexadecimal_code)

    int_code = 16
    hexadecimal_code = int_to_hexa(int_code)
    print(int_code, 'converts to', hexadecimal_code)

    int_code = 255
    hexadecimal_code = int_to_hexa(int_code)
    print(int_code, 'converts to', hexadecimal_code)
