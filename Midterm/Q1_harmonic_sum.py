#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:51:45 2024

@author: bing
"""


def harmonic_sum(n):
    if n == 1:
        return 1
    else:
        har_sum = harmonic_sum(n-1) + 1/n

    return har_sum


if __name__ == "__main__":
    print(harmonic_sum(2))
    print(harmonic_sum(5))
