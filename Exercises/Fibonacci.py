#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:20:20 2024

@author: kehanluo
"""


def fast_fib(n, memo={}):
    if n == 0 or n == 1:
        return 1
    # return fast_fib(n-1, memo)+fast_fib(n-2, memo)
    # This is normal Fibonacci

    try:
        return memo[n]
    except KeyError:
        memo[n] = fast_fib(n-1, memo)+fast_fib(n-2, memo)
        return memo[n]
    # This is fast Fibonacci


if __name__ == "__main__":
    print(fast_fib(5))
