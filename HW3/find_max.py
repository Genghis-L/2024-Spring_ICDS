#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 19:12:38 2017

@author: xg7
"""

# Q1


def order(p, q, n):
    # delete the following pass
    # and complete the function
    if p[n] > q[n]:
        return True
    else:
        return False


# Q2
def first_max(order_f, l, n):
    # delete the following pass
    # and complete the function
    first_max_pair = l[0]
    for i in range(1, len(l)):
        if order_f(l[i], first_max_pair, n):
            first_max_pair = l[i]
        else:
            continue

    return first_max_pair


# Q3
def last_max(order_f, l, n):
    # delete the following pass
    # and complete the function
    last_max_pair = l[-1]
    for i in range(-1, -len(l)-1, -1):
        if order_f(l[i], last_max_pair, n):
            last_max_pair = l[i]
        else:
            continue

    return last_max_pair


# testing part.
# You code should pass the tests and give the correst outputs.
# You can comment out them temporarily if you want.
if __name__ == "__main__":
    print("---testing---")
    result = order((1, 2, 3), (2, 1, 4), 0)
    print("order((1, 2, 3), (2, 1, 4), 0) returns:", result)
    result = order((1, 2, 3), (2, 1, 4), 1)
    print("order((1, 2, 3), (2, 1, 4), 1) returns:", result)
    result = order((1, 2, 3), (2, 1, 4), 2)
    print("order((1, 2, 3), (2, 1, 4), 2) returns:", result)
    t = [('X', 5), ('B', 6), ('P', 4), ('X', 3), ('B', 5), ('P', 6)]
    print("t =", t)
    print("first_max(order, t, 1) returns:")
    print(first_max(order, t, 1))
    print("Bonus: last_max(order, t, 1) returns:")
    print(last_max(order, t, 1))
