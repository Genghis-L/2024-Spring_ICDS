#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:15:18 2024

@author: bing
"""
import timeit


def selection_sort(lst):
    # lst is a list of N numbers.
    for i in range(len(lst)):
        min_j = i
        for j in range(i, len(lst)):
            if lst[j] < lst[min_j]:
                min_j = j
        lst[i], lst[min_j] = lst[min_j], lst[i]


if __name__ == "__main__":
    start = timeit.default_timer()

    lst = [10, 9, 5, 6, 8, 3, 2, 1, 4, 7]
    selection_sort(lst)
    print(lst)

    stop = timeit.default_timer()

    print("Time for Selection Sort:",stop-start)

    lst = [0, 1, 2, 3]
    selection_sort(lst)
    print(lst)
