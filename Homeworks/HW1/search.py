#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:45:30 2024

@author: bing
"""


def search(lst, n):
    loops = 0
    # input your code here
    for i in lst:
        loops += 1
        if n == i:
            return (True, loops)
    return (False, loops)


if __name__ == "__main__":

    integers = [99, 88, 77, 101, 203, 896, 555]
    print(search(integers, 101))
    print(search(integers, 1001))
