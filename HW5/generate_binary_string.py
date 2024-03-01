#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 20:40:42 2022

@author: bing
"""


def binary_string_without_consecutive_ones(n, binary_string=[], current_str=''):
    if n == 0:
        return []
    if n == 1:
        return ["0", "1"]

    current_lst = binary_string_without_consecutive_ones(n-1)
    binary_string = []

    for s in current_lst:
        temp = s + "0"
        binary_string.append(temp)
        if s[-1] != "1":
            temp = s + "1"
            binary_string.append(temp)

    return binary_string


if __name__ == "__main__":
    n = 3
    binary_string = []
    print(binary_string_without_consecutive_ones(n, binary_string))
    n = 4
    binary_string = []
    print(binary_string_without_consecutive_ones(n, binary_string))
