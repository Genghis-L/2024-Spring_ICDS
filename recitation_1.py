#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:54:12 2024

@author: kehanluo
"""

# Q1.2


def get_most_frequent_charcter(s):
    d = {}
    for c in s:
        d[c] = s.count(c)
    freq = max(d.values())
    for k in d:
        if d[k] == freq:
            print(k)
            break


get_most_frequent_charcter("taobao")


# Q2.1

def show_and_remove_larger_numbers(lst, n):
    for i in lst:
        if i > n:
            print(i, end='')

    print()

    for i in lst.copy():
        if i > n:
            lst.remove(i)
    print(lst)


lst = [2, 3, 5, 1, 2, 6, 3, 4, 4]
show_and_remove_larger_numbers(lst, 3)


# Q3.1

# def get_frequency(s):


def add_up():
    lst = []
    s = 0
    for i in range(1, n+1):
        s += i
        lst.append(i)
    print(sum(lst))
    print(s)


def add_up(n):
    if n == 0:
        return 0
    return add_up(n-1)+n


print(add_up(100))
