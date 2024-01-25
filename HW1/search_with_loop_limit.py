#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 16:36:21 2024

@author: bing
"""


def search_with_loop_limit(sorted_lst, n):
    loops = 0
   # input your code here
    l = len(sorted_lst)
    i = l//2
    while i in range(1, l-1):
        if n == sorted_lst[i]:
            return (True, loops)
        elif n > sorted_lst[i]:
            i = (i+l)//2
        elif n < sorted_lst[i]:
            i = i//2
        loops += 1

    if n == sorted_lst[0] or n == sorted_lst[l-1]:
        loops += 1
        return (True, loops)

    return (False, loops)


if __name__ == "__main__":

    integers = [77, 88, 99, 101, 203, 896, 555]
    print(search_with_loop_limit(integers, 101))
    print(search_with_loop_limit(integers, 1001))
