#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 01:04:02 2021

@author: bing
"""

def get_even_numbers(n):
    if n < 0:
        return []
    else:
        return [n] + get_even_numbers(n-2) if n % 2 == 0 else [n-1] + get_even_numbers(n-3)


## the followings are the tests your code should pass
## you may comment them out if you don't use them
if __name__ == "__main__":
    # for i in range(20):
        # print(i, get_even_numbers(i))
    print("n = {}, get_even_numbers({}) returns {}".format(0, 0, get_even_numbers(0)))
    print("n = {}, get_even_numbers({}) returns {}".format(1, 1, get_even_numbers(1)))
    print("n = {}, get_even_numbers({}) returns {}".format(20, 20, get_even_numbers(20)))
    print("n = {}, get_even_numbers({}) returns {}".format(21, 21, get_even_numbers(21)))
