#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:50:38 2024

@author: kehanluo
"""

'''
Suppose you want to count out a certain amount of money, say $123, using the fewest bills and coins. 
(Assume we are in China, we have 7 bills: 100, 50, 20, 10, 5, 2, and 1, and each bill is sufficient supply. )
'''


def minBills(bills, value):
    if value == 0:
        return [], 0
    num_current_picked = float("inf")
    for b in bills:
        if b <= value:
            p, num_last_picked = minBills(bills, value-b)
            if num_last_picked+1 < num_current_picked:
                num_current_picked = num_last_picked+1
                pk = p+[b]
    return pk, num_current_picked
# Brutal


def minBills_fst(bills, value, memo={}):
    if value == 0:
        return [], 0
    num_current_picked = float("inf")
    for b in bills:
        if b <= value:
            try:
                p, num_last_picked = memo[(b, value-b)]
            except KeyError:
                p, num_last_picked = minBills_fst(bills, value-b)
                memo[(b, value-b)] = p, num_last_picked
            if num_last_picked+1 < num_current_picked:
                num_current_picked = num_last_picked+1
                pk = p+[b]
    return pk, num_current_picked
# Fast


if __name__ == "__main__":

    bills = [9, 6, 5, 1]
    value = 11

    print("Brutal algorithm:")
    picked, n = minBills_fst(bills, value)
    print("The Bills I want to pick: {} \nThe total number is: {} \n".format(picked, n))

    print("Fast algorithm:")
    picked, n = minBills_fst(bills, value)
    print("The Bills I want to pick: {} \nThe total number is: {}".format(picked, n))
