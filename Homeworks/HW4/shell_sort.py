#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:06:22 2024

@author: bing
"""
# import timeit

def insertion_sort_with_gap(lst, g):
    # lst is a list of N numbers, and g is the gap
    for i in range(g, len(lst)):
        v = lst[i]
        j = i - g
        while j >= 0 and lst[j] > v:
            lst[j+g] = lst[j]
            j = j - g
        lst[j+g] = v


def shell_sort(lst):
    G = [5, 3, 1]
    # G is a list of M gaps in the descending order
    for i in range(0, len(G)):
        insertion_sort_with_gap(lst, G[i])


if __name__ == "__main__":
    # start = timeit.default_timer()

    lst = [10, 9, 5, 6, 8, 3, 2, 1, 4, 7]
    shell_sort(lst)
    print(lst)

    # stop = timeit.default_timer()

    # print("Time for Shell Sort:", stop-start)

    lst = [0, 1, 2, 3]
    shell_sort(lst)
    print(lst)
