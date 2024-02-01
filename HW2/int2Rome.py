#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 22:50:19 2020

@author: xg7
"""


def convert_to_Roman_numeral(n):
    romans_dict = {
        1000: 'M',
        900: 'CM',
        500: 'D',
        400: 'CD',
        100: 'C',
        90: 'XC',
        50: 'L',
        40: 'XL',
        10: 'X',
        9: 'IX',
        5: 'V',
        4: 'IV',
        1: 'I'
    }

    storage_list = []
    for value, char in romans_dict.items():
        number_of_char, n = divmod(n, value)
        storage_list.append(char * number_of_char)
        pass

    return ''.join(storage_list)


# test
if __name__ == "__main__":
    n = 1800
    print(convert_to_Roman_numeral(n))
