#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:50:15 2024

@author: bing
"""


def bSearch(L, e, low=0):
    """Assume L is a list, the elements of which are in ascending order.
    Returns the index of e if it is in L and -1 otherwise"""

    if len(L) == 1:
        if L[0] == e:
            return low
        else:
            return -1

    mid = len(L) // 2

    if L[mid] == e:
        return low+mid
    elif L[mid] > e:
        return bSearch(L[:mid], e, low)
    else:
        low += mid
        return bSearch(L[mid:], e, low)


if __name__ == "__main__":
    L = [i for i in range(10)]
    # random.shuffle(L)

    print("L:", L)
    e = 2
    print("e:", e)
    print(bSearch(L, e))
    e = 9
    print("e:", e)
    print(bSearch(L, e))
    e = 10
    print("e:", e)
    print(bSearch(L, e))
