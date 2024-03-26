#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:25:37 2024

@author: kehanluo
"""


def quicksort(seq):
    if len(seq) <= 1:
        return seq
    low, pivot, high = partition(seq)
    return quicksort(low)+[pivot]+quicksort(high)


def partition(seq):
    pivot, seq = seq[0], seq[1:]
    low = [x for x in seq if x <= pivot]
    high = [x for x in seq if x > pivot]
    return low, pivot, high


if __name__ == "__main__":
    seq = [1,2,4,4532,15,3215,3541,32,32,3,32,35,425,1]
    print(quicksort(seq))
