#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:54:12 2024

@author: kehanluo
"""


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


def get_most_frequent_charcter(s):
    ch = s[0]
    count = 0
    for c in s:
        if s.count(c) > count:
            ch = c
            count = s.count(c)
    print(ch)


get_most_frequent_charcter("aaabbbc,cc")


def show_and_remove_larger_numbers(lst, n):
    for i in lst:
        if i > n:
            print(i, end='')

    for i in lst.copy():
        if i > n:
            lst.remove(i)
    print(lst)


lst = [2, 3, 5, 1, 2, 6, 3, 4, 4]
show_and_remove_larger_numbers(lst, 3)


def get_frequency(s):
    d = dict()
    for c in s:
        if c.isalnum():
            d[c] = s.count(c)
    print(d)
    return d


get_frequency("NYU SHANGHAI!!!!!!")


x = 100


def func_1():
    print(x)


def func_2():
    x = 200

    def func(x):
        print(x)


def change(n):
    # n = ['Darth', 'Vader']
    n.clear()
    n.extend(['Darth', 'Vader'])


name = ['Skywalker', 'Anakin']
change(name)
print(name)


def add_up1(n):
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
    return add_up(n-1) + n


add_up(100)
